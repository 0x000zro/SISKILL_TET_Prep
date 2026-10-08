package com.tetprep.aspirant.ui.topic

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import com.tetprep.aspirant.data.local.entity.TopicEntity
import com.tetprep.aspirant.databinding.ActivityTopicExplorerBinding
import com.tetprep.aspirant.ui.study.MicroStudyActivity
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class TopicExplorerActivity : AppCompatActivity() {

    private lateinit var binding: ActivityTopicExplorerBinding
    private lateinit var adapter: TopicTreeAdapter
    private var subjectId: String = "CDP"

    // In-memory cache of tree structure
    private val rawTopics = mutableListOf<TopicEntity>()
    private val subtopicsByTopic = mutableMapOf<String, List<SubtopicEntity>>()
    private val microTopicsBySubtopic = mutableMapOf<String, List<MicroTopicEntity>>()
    private val expandedTopics = mutableSetOf<String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityTopicExplorerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        subjectId = intent.getStringExtra(Constants.EXTRA_SUBJECT_ID) ?: "CDP"
        val subjectName = intent.getStringExtra(Constants.EXTRA_SUBJECT_NAME) ?: "Subject Topics"

        binding.toolbarTopic.title = subjectName
        binding.toolbarTopic.setNavigationOnClickListener {
            finish()
        }

        setupRecyclerView()
        loadHierarchy()
    }

    private fun setupRecyclerView() {
        adapter = TopicTreeAdapter(
            onMicroTopicClick = { microTopic ->
                val intent = Intent(this, MicroStudyActivity::class.java).apply {
                    putExtra(Constants.EXTRA_MICRO_TOPIC_ID, microTopic.id)
                    putExtra(Constants.EXTRA_MICRO_TOPIC_TITLE, microTopic.nameHi)
                }
                startActivity(intent)
            },
            onTopicToggle = { topic, isExpanded ->
                if (isExpanded) {
                    expandedTopics.add(topic.id)
                } else {
                    expandedTopics.remove(topic.id)
                }
                rebuildTreeItems()
            }
        )

        binding.rvTopicTree.layoutManager = LinearLayoutManager(this)
        binding.rvTopicTree.adapter = adapter
    }

    private fun loadHierarchy() {
        val app = application as TetPrepApplication
        val repository = app.repository

        lifecycleScope.launch {
            val topics = withContext(Dispatchers.IO) {
                app.database.topicDao().getTopicsBySubjectDirect(subjectId)
            }

            rawTopics.clear()
            rawTopics.addAll(topics)

            // Default expand first 3 topics
            topics.take(3).forEach { expandedTopics.add(it.id) }

            withContext(Dispatchers.IO) {
                topics.forEach { topic ->
                    val subtopics = app.database.subtopicDao().getSubtopicsByTopicDirect(topic.id)
                    subtopicsByTopic[topic.id] = subtopics

                    subtopics.forEach { subtopic ->
                        val microTopics = app.database.microTopicDao().getMicroTopicsBySubtopicDirect(subtopic.id)
                        microTopicsBySubtopic[subtopic.id] = microTopics
                    }
                }
            }

            rebuildTreeItems()
        }
    }

    private fun rebuildTreeItems() {
        val treeList = mutableListOf<TreeItem>()
        rawTopics.forEach { topic ->
            val isExpanded = expandedTopics.contains(topic.id)
            treeList.add(TreeItem.TopicItem(topic, isExpanded))

            if (isExpanded) {
                val subtopics = subtopicsByTopic[topic.id] ?: emptyList()
                subtopics.forEach { subtopic ->
                    treeList.add(TreeItem.SubtopicItem(subtopic))

                    val microTopics = microTopicsBySubtopic[subtopic.id] ?: emptyList()
                    microTopics.forEach { micro ->
                        treeList.add(TreeItem.MicroTopicItem(micro, isCompleted = false))
                    }
                }
            }
        }
        adapter.submitTreeItems(treeList)
    }
}

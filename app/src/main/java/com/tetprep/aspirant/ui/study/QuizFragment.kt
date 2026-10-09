package com.tetprep.aspirant.ui.study

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentQuizBinding
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class QuizFragment : Fragment() {

    private var _binding: FragmentQuizBinding? = null
    private val binding get() = _binding!!
    private var microTopicId: String = ""
    private lateinit var adapter: ScrollableQuestionsAdapter
    private val bookmarkedIds = mutableSetOf<String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        microTopicId = arguments?.getString(ARG_MICRO_TOPIC_ID) ?: ""
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentQuizBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val app = requireActivity().application as TetPrepApplication
        val repository = app.repository

        setupRecyclerView(repository)
        loadQuestions(repository)
    }

    private fun setupRecyclerView(repository: com.tetprep.aspirant.data.repository.PedagogyRepository) {
        adapter = ScrollableQuestionsAdapter(
            onBookmarkToggle = { question ->
                viewLifecycleOwner.lifecycleScope.launch {
                    repository.toggleBookmark(question)
                    if (bookmarkedIds.contains(question.id)) {
                        bookmarkedIds.remove(question.id)
                        Toast.makeText(requireContext(), "Bookmark removed", Toast.LENGTH_SHORT).show()
                    } else {
                        bookmarkedIds.add(question.id)
                        Toast.makeText(requireContext(), "Bookmarked question", Toast.LENGTH_SHORT).show()
                    }
                }
            },
            isBookmarked = { id -> bookmarkedIds.contains(id) }
        )

        binding.rvQuestions.layoutManager = LinearLayoutManager(requireContext())
        binding.rvQuestions.adapter = adapter
    }

    private fun loadQuestions(repository: com.tetprep.aspirant.data.repository.PedagogyRepository) {
        viewLifecycleOwner.lifecycleScope.launch {
            binding.progressBar.visibility = View.VISIBLE

            // Pre-load bookmarks for instant icon status
            try {
                val bookmarks = repository.getAllBookmarks().first()
                bookmarkedIds.clear()
                bookmarks.forEach { bookmarkedIds.add(it.questionId) }
            } catch (e: Exception) {
                // Ignore bookmark load errors
            }

            // Prioritize downloaded OTA JSON cache -> bundled APK assets -> Room DB
            val questions = repository.loadQuestionsForMicroTopic(microTopicId, "MCQ")
            binding.progressBar.visibility = View.GONE

            if (questions.isNotEmpty()) {
                binding.tvQuestionCountBadge.text = "${questions.size} Questions"
                binding.rvQuestions.visibility = View.VISIBLE
                binding.layoutEmpty.visibility = View.GONE
                adapter.submitQuestions(questions)

                // Save completion progress
                repository.saveProgress(
                    microTopicId = microTopicId,
                    assetType = Constants.ASSET_MCQ,
                    isCompleted = true,
                    totalQuestions = questions.size
                )
            } else {
                binding.tvQuestionCountBadge.text = "0 Questions"
                binding.rvQuestions.visibility = View.GONE
                binding.layoutEmpty.visibility = View.VISIBLE
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val ARG_MICRO_TOPIC_ID = "arg_micro_topic_id"

        fun newInstance(microTopicId: String) = QuizFragment().apply {
            arguments = Bundle().apply {
                putString(ARG_MICRO_TOPIC_ID, microTopicId)
            }
        }
    }
}

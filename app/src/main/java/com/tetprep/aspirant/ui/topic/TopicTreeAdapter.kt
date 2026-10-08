package com.tetprep.aspirant.ui.topic

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.tetprep.aspirant.R
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import com.tetprep.aspirant.data.local.entity.TopicEntity
import com.tetprep.aspirant.databinding.ItemMicrotopicBinding
import com.tetprep.aspirant.databinding.ItemSubtopicHeaderBinding
import com.tetprep.aspirant.databinding.ItemTopicHeaderBinding

sealed class TreeItem {
    data class TopicItem(val topic: TopicEntity, var isExpanded: Boolean = true) : TreeItem()
    data class SubtopicItem(val subtopic: SubtopicEntity) : TreeItem()
    data class MicroTopicItem(val microTopic: MicroTopicEntity, val isCompleted: Boolean = false) : TreeItem()
}

class TopicTreeAdapter(
    private val onMicroTopicClick: (MicroTopicEntity) -> Unit,
    private val onTopicToggle: (TopicEntity, Boolean) -> Unit
) : RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    private val items = mutableListOf<TreeItem>()

    fun submitTreeItems(newItems: List<TreeItem>) {
        items.clear()
        items.addAll(newItems)
        notifyDataSetChanged()
    }

    override fun getItemViewType(position: Int): Int {
        return when (items[position]) {
            is TreeItem.TopicItem -> VIEW_TYPE_TOPIC
            is TreeItem.SubtopicItem -> VIEW_TYPE_SUBTOPIC
            is TreeItem.MicroTopicItem -> VIEW_TYPE_MICRO
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        return when (viewType) {
            VIEW_TYPE_TOPIC -> {
                val binding = ItemTopicHeaderBinding.inflate(inflater, parent, false)
                TopicViewHolder(binding, onTopicToggle)
            }
            VIEW_TYPE_SUBTOPIC -> {
                val binding = ItemSubtopicHeaderBinding.inflate(inflater, parent, false)
                SubtopicViewHolder(binding)
            }
            else -> {
                val binding = ItemMicrotopicBinding.inflate(inflater, parent, false)
                MicroTopicViewHolder(binding, onMicroTopicClick)
            }
        }
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        when (val item = items[position]) {
            is TreeItem.TopicItem -> (holder as TopicViewHolder).bind(item)
            is TreeItem.SubtopicItem -> (holder as SubtopicViewHolder).bind(item)
            is TreeItem.MicroTopicItem -> (holder as MicroTopicViewHolder).bind(item)
        }
    }

    override fun getItemCount(): Int = items.size

    class TopicViewHolder(
        private val binding: ItemTopicHeaderBinding,
        private val onTopicToggle: (TopicEntity, Boolean) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(item: TreeItem.TopicItem) {
            binding.tvTopicBadge.text = item.topic.code
            binding.tvTopicTitleHi.text = item.topic.titleHi
            binding.tvTopicTitleEn.text = item.topic.slug.replace("_", " ")

            binding.ivExpandTopic.rotation = if (item.isExpanded) 90f else -90f

            binding.root.setOnClickListener {
                item.isExpanded = !item.isExpanded
                binding.ivExpandTopic.rotation = if (item.isExpanded) 90f else -90f
                onTopicToggle(item.topic, item.isExpanded)
            }
        }
    }

    class SubtopicViewHolder(
        private val binding: ItemSubtopicHeaderBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(item: TreeItem.SubtopicItem) {
            binding.tvSubtopicTitle.text = "${item.subtopic.code}: ${item.subtopic.titleHi}"
        }
    }

    class MicroTopicViewHolder(
        private val binding: ItemMicrotopicBinding,
        private val onMicroTopicClick: (MicroTopicEntity) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(item: TreeItem.MicroTopicItem) {
            binding.tvMicroTitle.text = item.microTopic.nameHi
            val statusColor = if (item.isCompleted) R.color.palette_answered else R.color.palette_unanswered
            binding.ivCompletionStatus.imageTintList = ContextCompat.getColorStateList(binding.root.context, statusColor)

            binding.root.setOnClickListener {
                onMicroTopicClick(item.microTopic)
            }
        }
    }

    companion object {
        private const val VIEW_TYPE_TOPIC = 1
        private const val VIEW_TYPE_SUBTOPIC = 2
        private const val VIEW_TYPE_MICRO = 3
    }
}

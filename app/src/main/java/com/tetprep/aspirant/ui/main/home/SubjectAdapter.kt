package com.tetprep.aspirant.ui.main.home

import android.content.Context
import android.content.res.ColorStateList
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.tetprep.aspirant.R
import com.tetprep.aspirant.data.local.entity.SubjectEntity
import com.tetprep.aspirant.databinding.ItemSubjectCardBinding

class SubjectAdapter(
    private val onSubjectClick: (SubjectEntity) -> Unit
) : ListAdapter<SubjectEntity, SubjectAdapter.SubjectViewHolder>(DiffCallback) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): SubjectViewHolder {
        val binding = ItemSubjectCardBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return SubjectViewHolder(binding, onSubjectClick)
    }

    override fun onBindViewHolder(holder: SubjectViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class SubjectViewHolder(
        private val binding: ItemSubjectCardBinding,
        private val onSubjectClick: (SubjectEntity) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(subject: SubjectEntity) {
            val context = binding.root.context
            binding.tvSubjectNameEn.text = subject.nameEn
            binding.tvSubjectNameHi.text = subject.nameHi
            binding.tvTopicCount.text = "${subject.totalTopics} Topics"

            // Set subject icon and accents
            val (iconRes, colorRes) = getSubjectVisuals(subject.id)
            binding.ivSubjectIcon.setImageResource(iconRes)
            val color = ContextCompat.getColor(context, colorRes)
            binding.iconContainer.backgroundTintList = ColorStateList.valueOf(color).withAlpha(30)
            binding.ivSubjectIcon.imageTintList = ColorStateList.valueOf(color)

            binding.root.setOnClickListener {
                onSubjectClick(subject)
            }
        }

        private fun getSubjectVisuals(subjectId: String): Pair<Int, Int> {
            return when (subjectId.uppercase()) {
                "CDP" -> Pair(R.drawable.ic_cdp, R.color.subject_cdp)
                "HINDI" -> Pair(R.drawable.ic_hindi, R.color.subject_hindi)
                "MATH" -> Pair(R.drawable.ic_math, R.color.subject_math)
                "EVS" -> Pair(R.drawable.ic_evs, R.color.subject_evs)
                "ENG" -> Pair(R.drawable.ic_english, R.color.subject_english)
                "SAN" -> Pair(R.drawable.ic_sanskrit, R.color.subject_sanskrit)
                else -> Pair(R.drawable.ic_siskill_logo, R.color.primary)
            }
        }
    }

    companion object DiffCallback : DiffUtil.ItemCallback<SubjectEntity>() {
        override fun areItemsTheSame(oldItem: SubjectEntity, newItem: SubjectEntity): Boolean =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: SubjectEntity, newItem: SubjectEntity): Boolean =
            oldItem == newItem
    }
}

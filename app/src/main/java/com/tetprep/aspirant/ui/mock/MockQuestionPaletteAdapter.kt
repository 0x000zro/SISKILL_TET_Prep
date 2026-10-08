package com.tetprep.aspirant.ui.mock

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.tetprep.aspirant.R
import com.tetprep.aspirant.databinding.ItemPaletteNumberBinding

enum class QuestionStatus {
    UNVISITED,
    ANSWERED,
    MARKED_FOR_REVIEW
}

data class PaletteItem(
    val index: Int,
    var status: QuestionStatus = QuestionStatus.UNVISITED,
    var isCurrent: Boolean = false
)

class MockQuestionPaletteAdapter(
    private val onQuestionSelected: (Int) -> Unit
) : RecyclerView.Adapter<MockQuestionPaletteAdapter.PaletteViewHolder>() {

    private val items = mutableListOf<PaletteItem>()

    fun submitItems(newItems: List<PaletteItem>) {
        items.clear()
        items.addAll(newItems)
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PaletteViewHolder {
        val binding = ItemPaletteNumberBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return PaletteViewHolder(binding, onQuestionSelected)
    }

    override fun onBindViewHolder(holder: PaletteViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount(): Int = items.size

    class PaletteViewHolder(
        private val binding: ItemPaletteNumberBinding,
        private val onQuestionSelected: (Int) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(item: PaletteItem) {
            val context = binding.root.context
            binding.tvPaletteNumber.text = "${item.index + 1}"

            when {
                item.isCurrent -> {
                    binding.tvPaletteNumber.setBackgroundResource(R.drawable.bg_option_selected)
                    binding.tvPaletteNumber.setTextColor(ContextCompat.getColor(context, R.color.primary))
                }
                item.status == QuestionStatus.ANSWERED -> {
                    binding.tvPaletteNumber.setBackgroundResource(R.drawable.bg_option_correct)
                    binding.tvPaletteNumber.setTextColor(ContextCompat.getColor(context, R.color.palette_answered))
                }
                item.status == QuestionStatus.MARKED_FOR_REVIEW -> {
                    binding.tvPaletteNumber.setBackgroundResource(R.drawable.bg_option_selected)
                    binding.tvPaletteNumber.setTextColor(ContextCompat.getColor(context, R.color.palette_marked))
                }
                else -> {
                    binding.tvPaletteNumber.setBackgroundResource(R.drawable.bg_option_default)
                    binding.tvPaletteNumber.setTextColor(ContextCompat.getColor(context, R.color.on_surface_variant))
                }
            }

            binding.root.setOnClickListener {
                onQuestionSelected(item.index)
            }
        }
    }
}

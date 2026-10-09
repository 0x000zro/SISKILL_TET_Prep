package com.tetprep.aspirant.ui.study

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.tetprep.aspirant.R
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.databinding.ItemScrollableQuestionBinding

class ScrollableQuestionsAdapter(
    private val onBookmarkToggle: (QuestionEntity) -> Unit,
    private val isBookmarked: (String) -> Boolean = { false }
) : RecyclerView.Adapter<ScrollableQuestionsAdapter.QuestionViewHolder>() {

    private val questions = mutableListOf<QuestionEntity>()
    private val userSelections = mutableMapOf<Int, String>() // position -> selectedKey ("A", "B", "C", "D")

    fun submitQuestions(newQuestions: List<QuestionEntity>) {
        questions.clear()
        questions.addAll(newQuestions)
        userSelections.clear()
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): QuestionViewHolder {
        val binding = ItemScrollableQuestionBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return QuestionViewHolder(binding)
    }

    override fun onBindViewHolder(holder: QuestionViewHolder, position: Int) {
        holder.bind(questions[position], position)
    }

    override fun getItemCount(): Int = questions.size

    inner class QuestionViewHolder(
        private val binding: ItemScrollableQuestionBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(question: QuestionEntity, position: Int) {
            val context = binding.root.context

            // Badge / Header Counter
            val typePrefix = if (question.type.equals("PYQ", ignoreCase = true)) "PYQ" else "Question"
            binding.tvQuestionBadge.text = "$typePrefix ${position + 1} of ${questions.size}"

            // Bookmark button state
            val bookmarked = isBookmarked(question.id)
            binding.btnBookmark.setImageResource(
                if (bookmarked) R.drawable.ic_bookmark_saved else R.drawable.ic_bookmark
            )
            binding.btnBookmark.setOnClickListener {
                onBookmarkToggle(question)
                notifyItemChanged(position)
            }

            // 1. Question text
            binding.tvQuestionText.text = question.question

            // 2. Options (Option 1, Option 2, Option 3, Option 4)
            binding.tvOption1.text = "Option 1: ${question.optionA}"
            binding.tvOption2.text = "Option 2: ${question.optionB}"
            binding.tvOption3.text = "Option 3: ${question.optionC}"
            binding.tvOption4.text = "Option 4: ${question.optionD}"

            // Option selection click listeners
            val optionViews = listOf(
                Pair(binding.layoutOption1, "A"),
                Pair(binding.layoutOption2, "B"),
                Pair(binding.layoutOption3, "C"),
                Pair(binding.layoutOption4, "D")
            )

            val selectedKey = userSelections[position]
            updateOptionStyles(optionViews, question.answer, selectedKey)

            optionViews.forEach { (layout, key) ->
                layout.setOnClickListener {
                    userSelections[position] = key
                    updateOptionStyles(optionViews, question.answer, key)
                }
            }

            // 3. Correct Answer
            val correctOptionText = getAnswerFullText(question)
            binding.tvCorrectAnswer.text = "Option ${question.answer} — $correctOptionText"

            // 4. Exam Tag / Source (e.g., 'UPTET 2016')
            val displayExamTag = question.examTag.ifBlank {
                if (question.year != null) "UPTET / CTET ${question.year}" else "UPTET / CTET Official"
            }
            binding.tvExamTagSource.text = displayExamTag

            // 5. Detailed Explanation
            val explanation = question.explanation.ifBlank {
                "Detailed explanation is being compiled for this concept."
            }
            binding.tvDetailedExplanation.text = explanation
        }

        private fun updateOptionStyles(
            optionViews: List<Pair<LinearLayout, String>>,
            correctAnswerKey: String,
            selectedKey: String?
        ) {
            val normalizedCorrect = when (correctAnswerKey.uppercase().trim()) {
                "1" -> "A"
                "2" -> "B"
                "3" -> "C"
                "4" -> "D"
                else -> correctAnswerKey.take(1).uppercase()
            }

            optionViews.forEach { (layout, key) ->
                when {
                    selectedKey == null -> {
                        // Not yet answered by user: neutral default
                        layout.setBackgroundResource(R.drawable.bg_option_default)
                    }
                    key.equals(normalizedCorrect, ignoreCase = true) -> {
                        // The correct option is highlighted in green
                        layout.setBackgroundResource(R.drawable.bg_option_correct)
                    }
                    key.equals(selectedKey, ignoreCase = true) -> {
                        // User selected wrong option: highlight red
                        layout.setBackgroundResource(R.drawable.bg_option_wrong)
                    }
                    else -> {
                        layout.setBackgroundResource(R.drawable.bg_option_default)
                    }
                }
            }
        }

        private fun getAnswerFullText(q: QuestionEntity): String {
            return when (q.answer.uppercase().trim()) {
                "A", "1" -> q.optionA
                "B", "2" -> q.optionB
                "C", "3" -> q.optionC
                "D", "4" -> q.optionD
                else -> q.optionA
            }
        }
    }
}

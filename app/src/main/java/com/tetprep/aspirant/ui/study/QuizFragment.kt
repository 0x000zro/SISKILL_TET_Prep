package com.tetprep.aspirant.ui.study

import android.os.Bundle
import android.os.CountDownTimer
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.tetprep.aspirant.R
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.databinding.FragmentQuizBinding
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class QuizFragment : Fragment() {

    private var _binding: FragmentQuizBinding? = null
    private val binding get() = _binding!!
    private var microTopicId: String = ""

    private val questions = mutableListOf<QuestionEntity>()
    private var currentIndex = 0
    private var selectedOption: String? = null
    private var isAnswerChecked = false
    private var score = 0
    private var countDownTimer: CountDownTimer? = null

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

        setupOptionClicks()

        binding.btnCheckOrNext.setOnClickListener {
            if (!isAnswerChecked) {
                checkAnswer(repository)
            } else {
                nextQuestion(repository)
            }
        }

        binding.btnBookmark.setOnClickListener {
            if (currentIndex in questions.indices) {
                val currentQ = questions[currentIndex]
                viewLifecycleOwner.lifecycleScope.launch {
                    repository.toggleBookmark(currentQ)
                    Toast.makeText(requireContext(), "Bookmark updated", Toast.LENGTH_SHORT).show()
                }
            }
        }

        viewLifecycleOwner.lifecycleScope.launch {
            val qList = repository.getQuestionsByMicroTopicAndType(microTopicId, "MCQ").first()
            if (qList.isNotEmpty()) {
                questions.clear()
                questions.addAll(qList)
                showQuestion(0)
            } else {
                // If specific micro topic has no MCQs yet, load sample pedagogy MCQs
                val genericList = repository.getRandomPracticeQuestions("CDP", "MCQ", 5).first()
                if (genericList.isNotEmpty()) {
                    questions.clear()
                    questions.addAll(genericList)
                    showQuestion(0)
                } else {
                    binding.tvQuestionText.text = "MCQ questions are being updated for this micro-topic. Check back shortly!"
                    binding.btnCheckOrNext.isEnabled = false
                }
            }
        }
    }

    private fun setupOptionClicks() {
        val options = listOf(
            Triple(binding.layoutOptionA, "A", binding.badgeOptionA),
            Triple(binding.layoutOptionB, "B", binding.badgeOptionB),
            Triple(binding.layoutOptionC, "C", binding.badgeOptionC),
            Triple(binding.layoutOptionD, "D", binding.badgeOptionD)
        )

        options.forEach { (layout, key, _) ->
            layout.setOnClickListener {
                if (!isAnswerChecked) {
                    selectedOption = key
                    updateOptionSelections(key)
                }
            }
        }
    }

    private fun updateOptionSelections(selectedKey: String) {
        val list = listOf(
            Pair(binding.layoutOptionA, "A"),
            Pair(binding.layoutOptionB, "B"),
            Pair(binding.layoutOptionC, "C"),
            Pair(binding.layoutOptionD, "D")
        )

        list.forEach { (layout, key) ->
            if (key == selectedKey) {
                layout.setBackgroundResource(R.drawable.bg_option_selected)
            } else {
                layout.setBackgroundResource(R.drawable.bg_option_default)
            }
        }
    }

    private fun showQuestion(index: Int) {
        if (index !in questions.indices) return
        currentIndex = index
        val q = questions[index]
        selectedOption = null
        isAnswerChecked = false

        binding.tvQuestionCounter.text = "Question ${index + 1} of ${questions.size}"
        binding.tvQuestionText.text = q.question
        binding.tvOptionA.text = q.optionA
        binding.tvOptionB.text = q.optionB
        binding.tvOptionC.text = q.optionC
        binding.tvOptionD.text = q.optionD

        // Reset backgrounds
        binding.layoutOptionA.setBackgroundResource(R.drawable.bg_option_default)
        binding.layoutOptionB.setBackgroundResource(R.drawable.bg_option_default)
        binding.layoutOptionC.setBackgroundResource(R.drawable.bg_option_default)
        binding.layoutOptionD.setBackgroundResource(R.drawable.bg_option_default)

        binding.cardExplanation.visibility = View.GONE
        binding.btnCheckOrNext.text = getString(R.string.action_check_answer)

        startTimer()
    }

    private fun startTimer() {
        countDownTimer?.cancel()
        countDownTimer = object : CountDownTimer(30000, 1000) {
            override fun onTick(millisUntilFinished: Long) {
                val sec = millisUntilFinished / 1000
                binding.tvTimer.text = String.format("00:%02d", sec)
            }

            override fun onFinish() {
                binding.tvTimer.text = "00:00"
                if (!isAnswerChecked) {
                    val app = requireActivity().application as TetPrepApplication
                    checkAnswer(app.repository)
                }
            }
        }.start()
    }

    private fun checkAnswer(repository: com.tetprep.aspirant.data.repository.PedagogyRepository) {
        countDownTimer?.cancel()
        if (currentIndex !in questions.indices) return
        val q = questions[currentIndex]
        isAnswerChecked = true

        val isCorrect = selectedOption?.equals(q.answer, ignoreCase = true) == true
        if (isCorrect) {
            score++
        }

        // Highlight correct and wrong options
        highlightAnswerResults(q.answer, selectedOption)

        binding.cardExplanation.visibility = View.VISIBLE
        binding.tvResultVerdict.text = if (isCorrect) "✓ Correct! (Option ${q.answer})" else "✗ Incorrect. Correct Option is ${q.answer}"
        binding.tvResultVerdict.setTextColor(
            ContextCompat.getColor(
                requireContext(),
                if (isCorrect) R.color.palette_answered else R.color.option_wrong_stroke
            )
        )
        binding.tvExplanationText.text = "${q.explanation}\n\n[Bloom's Taxonomy: ${q.bloomTaxonomyLevel ?: "Understanding"}]"

        binding.btnCheckOrNext.text = if (currentIndex < questions.size - 1) getString(R.string.action_next) else "Finish Quiz"
    }

    private fun highlightAnswerResults(correctKey: String, selectedKey: String?) {
        val map = mapOf(
            "A" to binding.layoutOptionA,
            "B" to binding.layoutOptionB,
            "C" to binding.layoutOptionC,
            "D" to binding.layoutOptionD
        )

        map.forEach { (key, layout) ->
            if (key.equals(correctKey, ignoreCase = true)) {
                layout.setBackgroundResource(R.drawable.bg_option_correct)
            } else if (key.equals(selectedKey, ignoreCase = true)) {
                layout.setBackgroundResource(R.drawable.bg_option_wrong)
            } else {
                layout.setBackgroundResource(R.drawable.bg_option_default)
            }
        }
    }

    private fun nextQuestion(repository: com.tetprep.aspirant.data.repository.PedagogyRepository) {
        if (currentIndex < questions.size - 1) {
            showQuestion(currentIndex + 1)
        } else {
            // Save final progress
            viewLifecycleOwner.lifecycleScope.launch {
                repository.saveProgress(
                    microTopicId,
                    Constants.ASSET_MCQ,
                    isCompleted = true,
                    score = score,
                    totalQuestions = questions.size
                )
            }
            Toast.makeText(
                requireContext(),
                "Quiz Completed! Score: $score / ${questions.size}",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        countDownTimer?.cancel()
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

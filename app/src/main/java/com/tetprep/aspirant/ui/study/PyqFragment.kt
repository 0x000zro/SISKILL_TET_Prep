package com.tetprep.aspirant.ui.study

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.databinding.FragmentPyqBinding
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class PyqFragment : Fragment() {

    private var _binding: FragmentPyqBinding? = null
    private val binding get() = _binding!!
    private var microTopicId: String = ""

    private val pyqList = mutableListOf<QuestionEntity>()
    private var currentIndex = 0
    private var isAnswerRevealed = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        microTopicId = arguments?.getString(ARG_MICRO_TOPIC_ID) ?: ""
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentPyqBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val app = requireActivity().application as TetPrepApplication
        val repository = app.repository

        binding.btnPyqReveal.setOnClickListener {
            toggleRevealAnswer()
        }

        binding.btnPyqPrev.setOnClickListener {
            if (currentIndex > 0) {
                showPyq(currentIndex - 1)
            }
        }

        binding.btnPyqNext.setOnClickListener {
            if (currentIndex < pyqList.size - 1) {
                showPyq(currentIndex + 1)
            }
        }

        binding.btnPyqBookmark.setOnClickListener {
            if (currentIndex in pyqList.indices) {
                val q = pyqList[currentIndex]
                viewLifecycleOwner.lifecycleScope.launch {
                    repository.toggleBookmark(q)
                    Toast.makeText(requireContext(), "Bookmark updated", Toast.LENGTH_SHORT).show()
                }
            }
        }

        viewLifecycleOwner.lifecycleScope.launch {
            val list = repository.getQuestionsByMicroTopicAndType(microTopicId, "PYQ").first()
            if (list.isNotEmpty()) {
                pyqList.clear()
                pyqList.addAll(list)
                showPyq(0)
            } else {
                val genericPyq = repository.getRandomPracticeQuestions("CDP", "PYQ", 5).first()
                if (genericPyq.isNotEmpty()) {
                    pyqList.clear()
                    pyqList.addAll(genericPyq)
                    showPyq(0)
                } else {
                    binding.tvPyqQuestionText.text = "Official PYQs are being linked for this micro-topic. Check back shortly!"
                    binding.btnPyqReveal.isEnabled = false
                }
            }
        }
    }

    private fun showPyq(index: Int) {
        if (index !in pyqList.indices) return
        currentIndex = index
        val q = pyqList[index]
        isAnswerRevealed = false

        binding.tvPyqExamTag.text = q.examTag
        binding.tvPyqCounter.text = "PYQ ${index + 1} of ${pyqList.size}"
        binding.tvPyqQuestionText.text = q.question
        binding.tvPyqOptionA.text = "(A) ${q.optionA}"
        binding.tvPyqOptionB.text = "(B) ${q.optionB}"
        binding.tvPyqOptionC.text = "(C) ${q.optionC}"
        binding.tvPyqOptionD.text = "(D) ${q.optionD}"

        binding.cardPyqSolution.visibility = View.GONE
        binding.btnPyqReveal.text = "Reveal Official Key"

        binding.btnPyqPrev.isEnabled = index > 0
        binding.btnPyqNext.isEnabled = index < pyqList.size - 1

        // Record progress
        val app = requireActivity().application as TetPrepApplication
        viewLifecycleOwner.lifecycleScope.launch {
            app.repository.saveProgress(microTopicId, Constants.ASSET_PYQ, isCompleted = true)
        }
    }

    private fun toggleRevealAnswer() {
        if (currentIndex !in pyqList.indices) return
        val q = pyqList[currentIndex]
        isAnswerRevealed = !isAnswerRevealed

        if (isAnswerRevealed) {
            binding.cardPyqSolution.visibility = View.VISIBLE
            binding.tvPyqOfficialKey.text = "Official Key: Option ${q.answer}"
            binding.tvPyqExplanation.text = "${q.explanation}\n\n[Exam: ${q.examTag}]"
            binding.btnPyqReveal.text = "Hide Solution"
        } else {
            binding.cardPyqSolution.visibility = View.GONE
            binding.btnPyqReveal.text = "Reveal Official Key"
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val ARG_MICRO_TOPIC_ID = "arg_micro_topic_id"

        fun newInstance(microTopicId: String) = PyqFragment().apply {
            arguments = Bundle().apply {
                putString(ARG_MICRO_TOPIC_ID, microTopicId)
            }
        }
    }
}

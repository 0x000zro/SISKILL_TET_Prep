package com.tetprep.aspirant.ui.study

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentPracticeWorksheetBinding
import com.tetprep.aspirant.utils.Constants
import com.tetprep.aspirant.utils.MarkdownRenderer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class PracticeWorksheetFragment : Fragment() {

    private var _binding: FragmentPracticeWorksheetBinding? = null
    private val binding get() = _binding!!
    private var microTopicId: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        microTopicId = arguments?.getString(ARG_MICRO_TOPIC_ID) ?: ""
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentPracticeWorksheetBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val app = requireActivity().application as TetPrepApplication
        val repository = app.repository
        val markdownRenderer = MarkdownRenderer.getInstance(requireContext())

        lifecycleScope.launch {
            val microTopic = withContext(Dispatchers.IO) {
                repository.getMicroTopicByIdDirect(microTopicId)
            }

            val content = withContext(Dispatchers.IO) {
                repository.readMarkdownContent(microTopic?.practicePath)
            }

            markdownRenderer.render(binding.tvPracticeMarkdown, content)

            // Mark completed
            repository.saveProgress(microTopicId, Constants.ASSET_PRACTICE, isCompleted = true)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val ARG_MICRO_TOPIC_ID = "arg_micro_topic_id"

        fun newInstance(microTopicId: String) = PracticeWorksheetFragment().apply {
            arguments = Bundle().apply {
                putString(ARG_MICRO_TOPIC_ID, microTopicId)
            }
        }
    }
}

package com.tetprep.aspirant.ui.study

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.widget.NestedScrollView
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentConceptBinding
import com.tetprep.aspirant.utils.Constants
import com.tetprep.aspirant.utils.MarkdownRenderer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ConceptFragment : Fragment() {

    private var _binding: FragmentConceptBinding? = null
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
        _binding = FragmentConceptBinding.inflate(inflater, container, false)
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
                repository.readMarkdownContent(microTopic?.conceptPath)
            }

            markdownRenderer.render(binding.tvConceptMarkdown, content)
        }

        // Reading scroll progress tracker
        binding.scrollConcept.setOnScrollChangeListener(
            NestedScrollView.OnScrollChangeListener { _, _, scrollY, _, _ ->
                val totalScroll = binding.scrollConcept.getChildAt(0).measuredHeight - binding.scrollConcept.measuredHeight
                if (totalScroll > 0) {
                    val progress = (scrollY * 100) / totalScroll
                    binding.readingProgress.progress = progress

                    if (progress >= 90) {
                        viewLifecycleOwner.lifecycleScope.launch {
                            repository.saveProgress(microTopicId, Constants.ASSET_CONCEPT, isCompleted = true)
                        }
                    }
                }
            }
        )
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val ARG_MICRO_TOPIC_ID = "arg_micro_topic_id"

        fun newInstance(microTopicId: String) = ConceptFragment().apply {
            arguments = Bundle().apply {
                putString(ARG_MICRO_TOPIC_ID, microTopicId)
            }
        }
    }
}

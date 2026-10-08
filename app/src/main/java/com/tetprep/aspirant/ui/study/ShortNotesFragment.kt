package com.tetprep.aspirant.ui.study

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.tetprep.aspirant.R
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentShortNotesBinding
import com.tetprep.aspirant.utils.Constants
import com.tetprep.aspirant.utils.MarkdownRenderer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ShortNotesFragment : Fragment() {

    private var _binding: FragmentShortNotesBinding? = null
    private val binding get() = _binding!!
    private var microTopicId: String = ""
    private var notesContent: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        microTopicId = arguments?.getString(ARG_MICRO_TOPIC_ID) ?: ""
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentShortNotesBinding.inflate(inflater, container, false)
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

            notesContent = withContext(Dispatchers.IO) {
                repository.readMarkdownContent(microTopic?.shortNotesPath)
            }

            markdownRenderer.render(binding.tvNotesMarkdown, notesContent)

            // Mark completed
            repository.saveProgress(microTopicId, Constants.ASSET_SHORT_NOTES, isCompleted = true)
        }

        binding.btnCopyNotes.setOnClickListener {
            if (notesContent.isNotEmpty()) {
                val clipboard = requireContext().getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip = ClipData.newPlainText("SISKILL Notes", notesContent)
                clipboard.setPrimaryClip(clip)
                Toast.makeText(requireContext(), R.string.copied_to_clipboard, Toast.LENGTH_SHORT).show()
            }
        }

        binding.btnShareNotes.setOnClickListener {
            if (notesContent.isNotEmpty()) {
                val sendIntent = Intent().apply {
                    action = Intent.ACTION_SEND
                    putExtra(Intent.EXTRA_TEXT, "SISKILL TET Notes:\n\n$notesContent")
                    type = "text/plain"
                }
                val shareIntent = Intent.createChooser(sendIntent, "Share Revision Notes")
                startActivity(shareIntent)
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val ARG_MICRO_TOPIC_ID = "arg_micro_topic_id"

        fun newInstance(microTopicId: String) = ShortNotesFragment().apply {
            arguments = Bundle().apply {
                putString(ARG_MICRO_TOPIC_ID, microTopicId)
            }
        }
    }
}

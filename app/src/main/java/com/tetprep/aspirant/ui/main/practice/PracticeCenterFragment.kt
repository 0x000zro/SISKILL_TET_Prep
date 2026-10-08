package com.tetprep.aspirant.ui.main.practice

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.tetprep.aspirant.databinding.FragmentPracticeCenterBinding
import com.tetprep.aspirant.ui.mock.MockTestActivity
import com.tetprep.aspirant.utils.Constants

class PracticeCenterFragment : Fragment() {

    private var _binding: FragmentPracticeCenterBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentPracticeCenterBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.btnStartMockTest.setOnClickListener {
            launchMockTest()
        }

        binding.cardMockTest.setOnClickListener {
            launchMockTest()
        }

        binding.cardQuickQuiz.setOnClickListener {
            Toast.makeText(requireContext(), "Select any topic from Subjects tab to start instant MCQ quiz!", Toast.LENGTH_SHORT).show()
        }

        binding.cardPyqArchive.setOnClickListener {
            Toast.makeText(requireContext(), "Explore PYQ Vault inside any subject micro-topic!", Toast.LENGTH_SHORT).show()
        }
    }

    private fun launchMockTest() {
        val intent = Intent(requireContext(), MockTestActivity::class.java).apply {
            putExtra(Constants.EXTRA_MOCK_TEST_ID, "MOCK_CTET_PAPER1_FULL")
        }
        startActivity(intent)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

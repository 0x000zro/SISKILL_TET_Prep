package com.tetprep.aspirant.ui.main.home

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentSubjectsBinding
import com.tetprep.aspirant.ui.topic.TopicExplorerActivity
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class SubjectsFragment : Fragment() {

    private var _binding: FragmentSubjectsBinding? = null
    private val binding get() = _binding!!
    private lateinit var adapter: SubjectAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSubjectsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val app = requireActivity().application as TetPrepApplication
        val repository = app.repository

        adapter = SubjectAdapter { subject ->
            val intent = Intent(requireContext(), TopicExplorerActivity::class.java).apply {
                putExtra(Constants.EXTRA_SUBJECT_ID, subject.id)
                putExtra(Constants.EXTRA_SUBJECT_NAME, subject.nameEn)
            }
            startActivity(intent)
        }

        binding.rvSubjects.layoutManager = LinearLayoutManager(requireContext())
        binding.rvSubjects.adapter = adapter

        viewLifecycleOwner.lifecycleScope.launch {
            repository.getAllSubjects().collectLatest { subjects ->
                adapter.submitList(subjects)
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

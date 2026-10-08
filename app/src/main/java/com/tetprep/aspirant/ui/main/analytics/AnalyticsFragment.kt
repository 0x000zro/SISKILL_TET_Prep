package com.tetprep.aspirant.ui.main.analytics

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentAnalyticsBinding
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class AnalyticsFragment : Fragment() {

    private var _binding: FragmentAnalyticsBinding? = null
    private val binding get() = _binding!!
    private lateinit var adapter: BookmarksAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentAnalyticsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val app = requireActivity().application as TetPrepApplication
        val repository = app.repository

        adapter = BookmarksAdapter { bookmark ->
            viewLifecycleOwner.lifecycleScope.launch {
                repository.deleteBookmark(bookmark.questionId)
            }
        }

        binding.rvBookmarks.layoutManager = LinearLayoutManager(requireContext())
        binding.rvBookmarks.adapter = adapter

        // Observe completed micro topics
        viewLifecycleOwner.lifecycleScope.launch {
            repository.getCompletedMicroTopicCount().collectLatest { count ->
                binding.tvCompletedCount.text = count.toString()
            }
        }

        // Observe quiz accuracy
        viewLifecycleOwner.lifecycleScope.launch {
            repository.getTotalQuizScore().collectLatest { totalScore ->
                repository.getTotalAttemptedQuestions().collectLatest { totalAttempted ->
                    val score = totalScore ?: 0
                    val attempted = totalAttempted ?: 0
                    val accuracy = if (attempted > 0) (score * 100 / attempted) else 0
                    binding.tvAccuracyRate.text = "$accuracy%"
                }
            }
        }

        // Observe bookmarks
        viewLifecycleOwner.lifecycleScope.launch {
            repository.getAllBookmarks().collectLatest { bookmarks ->
                adapter.submitList(bookmarks)
                binding.tvNoBookmarks.visibility = if (bookmarks.isEmpty()) View.VISIBLE else View.GONE
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

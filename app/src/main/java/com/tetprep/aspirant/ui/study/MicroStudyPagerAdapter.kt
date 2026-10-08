package com.tetprep.aspirant.ui.study

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter

class MicroStudyPagerAdapter(
    activity: FragmentActivity,
    private val microTopicId: String
) : FragmentStateAdapter(activity) {

    override fun getItemCount(): Int = 5

    override fun createFragment(position: Int): Fragment {
        return when (position) {
            0 -> ConceptFragment.newInstance(microTopicId)
            1 -> ShortNotesFragment.newInstance(microTopicId)
            2 -> QuizFragment.newInstance(microTopicId)
            3 -> PyqFragment.newInstance(microTopicId)
            4 -> PracticeWorksheetFragment.newInstance(microTopicId)
            else -> ConceptFragment.newInstance(microTopicId)
        }
    }
}

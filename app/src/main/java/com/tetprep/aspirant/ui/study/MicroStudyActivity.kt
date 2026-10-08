package com.tetprep.aspirant.ui.study

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.tabs.TabLayoutMediator
import com.tetprep.aspirant.R
import com.tetprep.aspirant.databinding.ActivityMicroStudyBinding
import com.tetprep.aspirant.utils.Constants

class MicroStudyActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMicroStudyBinding
    private var microTopicId: String = ""
    private var microTopicTitle: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMicroStudyBinding.inflate(layoutInflater)
        setContentView(binding.root)

        microTopicId = intent.getStringExtra(Constants.EXTRA_MICRO_TOPIC_ID) ?: ""
        microTopicTitle = intent.getStringExtra(Constants.EXTRA_MICRO_TOPIC_TITLE) ?: "Study Room"

        binding.toolbarStudy.title = microTopicTitle
        binding.toolbarStudy.setNavigationOnClickListener {
            finish()
        }

        setupViewPager()
    }

    private fun setupViewPager() {
        val adapter = MicroStudyPagerAdapter(this, microTopicId)
        binding.viewPagerStudy.adapter = adapter

        val tabTitles = arrayOf(
            getString(R.string.tab_concept),
            getString(R.string.tab_short_notes),
            getString(R.string.tab_mcq),
            getString(R.string.tab_pyq),
            getString(R.string.tab_practice)
        )

        TabLayoutMediator(binding.tabLayoutStudy, binding.viewPagerStudy) { tab, position ->
            tab.text = tabTitles[position]
        }.attach()
    }
}

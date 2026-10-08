package com.tetprep.aspirant.ui.main

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.tetprep.aspirant.R
import com.tetprep.aspirant.databinding.ActivityMainBinding
import com.tetprep.aspirant.ui.main.analytics.AnalyticsFragment
import com.tetprep.aspirant.ui.main.home.SubjectsFragment
import com.tetprep.aspirant.ui.main.practice.PracticeCenterFragment
import com.tetprep.aspirant.ui.main.settings.SettingsFragment

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupBottomNavigation()

        if (savedInstanceState == null) {
            loadFragment(SubjectsFragment())
        }
    }

    private fun setupBottomNavigation() {
        binding.bottomNavigation.setOnItemSelectedListener { item ->
            val fragment: Fragment = when (item.itemId) {
                R.id.nav_home -> SubjectsFragment()
                R.id.nav_practice -> PracticeCenterFragment()
                R.id.nav_analytics -> AnalyticsFragment()
                R.id.nav_settings -> SettingsFragment()
                else -> SubjectsFragment()
            }
            loadFragment(fragment)
            true
        }
    }

    private fun loadFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragmentContainer, fragment)
            .commit()
    }
}

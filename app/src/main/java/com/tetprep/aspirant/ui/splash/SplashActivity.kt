package com.tetprep.aspirant.ui.splash

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.data.local.AssetPreloader
import com.tetprep.aspirant.databinding.ActivitySplashBinding
import com.tetprep.aspirant.ui.main.MainActivity
import kotlinx.coroutines.launch

@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySplashBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySplashBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val app = application as TetPrepApplication
        val preloader = AssetPreloader(this, app.database, app.preferences)

        lifecycleScope.launch {
            binding.progressBar.isIndeterminate = false
            binding.progressBar.max = 100

            val success = preloader.preloadIfNeeded { progress, message ->
                runOnUiThread {
                    binding.progressBar.progress = progress
                    binding.tvStatus.text = message
                }
            }

            if (success) {
                startActivity(Intent(this@SplashActivity, MainActivity::class.java))
                finish()
            } else {
                binding.tvStatus.text = "Error initializing repository. Retrying..."
                startActivity(Intent(this@SplashActivity, MainActivity::class.java))
                finish()
            }
        }
    }
}

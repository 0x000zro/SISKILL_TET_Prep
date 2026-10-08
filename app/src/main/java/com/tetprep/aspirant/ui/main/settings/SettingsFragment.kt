package com.tetprep.aspirant.ui.main.settings

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.tetprep.aspirant.R
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.databinding.FragmentSettingsBinding
import com.tetprep.aspirant.sync.GitHubContentSyncService
import com.tetprep.aspirant.sync.SyncResult
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class SettingsFragment : Fragment() {

    private var _binding: FragmentSettingsBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSettingsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val app = requireActivity().application as TetPrepApplication
        val preferences = app.preferences

        updateUiFromPreferences()

        binding.btnCheckUpdates.setOnClickListener {
            performSync(app)
        }
    }

    private fun updateUiFromPreferences() {
        val app = requireActivity().application as TetPrepApplication
        val preferences = app.preferences

        binding.tvLocalVersion.text = "Local Manifest Version: ${preferences.localVersion}"

        val lastSync = if (preferences.lastSyncTimestamp > 0) {
            val sdf = SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.getDefault())
            sdf.format(Date(preferences.lastSyncTimestamp))
        } else {
            "Bundled Assets Initialized"
        }
        binding.tvLastSynced.text = "Last Synced: $lastSync"
    }

    private fun performSync(app: TetPrepApplication) {
        val syncDialogView = LayoutInflater.from(requireContext())
            .inflate(R.layout.dialog_sync_progress, null)

        val tvDialogMessage = syncDialogView.findViewById<TextView>(R.id.tvSyncDialogMessage)
        val progressBar = syncDialogView.findViewById<LinearProgressIndicator>(R.id.syncProgressBar)
        val tvPercentage = syncDialogView.findViewById<TextView>(R.id.tvSyncProgressPercentage)

        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setView(syncDialogView)
            .setCancelable(false)
            .setNegativeButton("Dismiss", null)
            .create()

        dialog.show()

        val syncService = GitHubContentSyncService(requireContext(), app.database, app.preferences)

        viewLifecycleOwner.lifecycleScope.launch {
            val result = syncService.syncContent { progress, message ->
                requireActivity().runOnUiThread {
                    progressBar.isIndeterminate = false
                    progressBar.progress = progress
                    tvDialogMessage.text = message
                    tvPercentage.text = "$progress%"
                }
            }

            dialog.dismiss()
            updateUiFromPreferences()

            when (result) {
                is SyncResult.Success -> {
                    MaterialAlertDialogBuilder(requireContext())
                        .setTitle("Update Successful")
                        .setMessage("Repository content updated to version ${result.newVersion}!")
                        .setPositiveButton("OK", null)
                        .show()
                }
                is SyncResult.AlreadyUpToDate -> {
                    Toast.makeText(requireContext(), "Content is up to date (Version ${result.currentVersion})", Toast.LENGTH_SHORT).show()
                }
                is SyncResult.Failure -> {
                    MaterialAlertDialogBuilder(requireContext())
                        .setTitle("Offline Mode Active")
                        .setMessage("${result.error}\n\nThe app will continue operating normally with 100% full local bundled content.")
                        .setPositiveButton("Understood", null)
                        .show()
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

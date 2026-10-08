package com.tetprep.aspirant.sync

import android.content.Context
import android.util.Log
import androidx.work.Constraints
import androidx.work.CoroutineWorker
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.NetworkType
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import com.tetprep.aspirant.data.local.AppDatabase
import com.tetprep.aspirant.data.local.AppPreferencesRepository
import java.util.concurrent.TimeUnit

class ContentSyncWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        Log.d(TAG, "ContentSyncWorker triggered in background.")
        val database = AppDatabase.getInstance(applicationContext)
        val preferences = AppPreferencesRepository(applicationContext)
        val syncService = GitHubContentSyncService(applicationContext, database, preferences)

        return when (val result = syncService.syncContent()) {
            is SyncResult.Success -> {
                Log.i(TAG, "Background sync updated to ${result.newVersion}")
                Result.success()
            }
            is SyncResult.AlreadyUpToDate -> {
                Log.d(TAG, "Background sync: Already up to date")
                Result.success()
            }
            is SyncResult.Failure -> {
                Log.w(TAG, "Background sync error: ${result.error}")
                if (runAttemptCount < 3) Result.retry() else Result.failure()
            }
        }
    }

    companion object {
        private const val TAG = "ContentSyncWorker"
        private const val WORK_NAME = "periodic_content_sync_work"

        fun schedulePeriodicSync(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build()

            val syncRequest = PeriodicWorkRequestBuilder<ContentSyncWorker>(24, TimeUnit.HOURS)
                .setConstraints(constraints)
                .build()

            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                WORK_NAME,
                ExistingPeriodicWorkPolicy.KEEP,
                syncRequest
            )
            Log.d(TAG, "Scheduled periodic WorkManager content sync.")
        }
    }
}

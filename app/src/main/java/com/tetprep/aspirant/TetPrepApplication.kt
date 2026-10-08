package com.tetprep.aspirant

import android.app.Application
import com.tetprep.aspirant.data.local.AppDatabase
import com.tetprep.aspirant.data.local.AppPreferencesRepository
import com.tetprep.aspirant.data.repository.PedagogyRepository
import com.tetprep.aspirant.sync.ContentSyncWorker

class TetPrepApplication : Application() {

    lateinit var database: AppDatabase
        private set

    lateinit var preferences: AppPreferencesRepository
        private set

    lateinit var repository: PedagogyRepository
        private set

    override fun onCreate() {
        super.onCreate()
        instance = this

        database = AppDatabase.getInstance(this)
        preferences = AppPreferencesRepository(this)
        repository = PedagogyRepository(this, database, preferences)

        // Schedule periodic non-blocking background check
        ContentSyncWorker.schedulePeriodicSync(this)
    }

    companion object {
        lateinit var instance: TetPrepApplication
            private set
    }
}

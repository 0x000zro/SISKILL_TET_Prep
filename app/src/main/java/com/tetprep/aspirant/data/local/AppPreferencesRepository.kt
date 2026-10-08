package com.tetprep.aspirant.data.local

import android.content.Context
import android.content.SharedPreferences
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow

class AppPreferencesRepository(context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences(Constants.PREFERENCES_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val KEY_LOCAL_VERSION = "key_local_version"
        private const val KEY_LAST_SYNC_TIME = "key_last_sync_time"
        private const val KEY_IS_INITIALIZED = "key_is_initialized"
        private const val KEY_SELECTED_LANGUAGE = "key_selected_language"
        private const val KEY_THEME_MODE = "key_theme_mode"
        private const val KEY_LAST_SYNC_STATUS = "key_last_sync_status"
    }

    var localVersion: String
        get() = prefs.getString(KEY_LOCAL_VERSION, "0.0.0") ?: "0.0.0"
        set(value) = prefs.edit().putString(KEY_LOCAL_VERSION, value).apply()

    var lastSyncTimestamp: Long
        get() = prefs.getLong(KEY_LAST_SYNC_TIME, 0L)
        set(value) = prefs.edit().putLong(KEY_LAST_SYNC_TIME, value).apply()

    var isInitialized: Boolean
        get() = prefs.getBoolean(KEY_IS_INITIALIZED, false)
        set(value) = prefs.edit().putBoolean(KEY_IS_INITIALIZED, value).apply()

    var selectedLanguage: String
        get() = prefs.getString(KEY_SELECTED_LANGUAGE, "hi") ?: "hi"
        set(value) = prefs.edit().putString(KEY_SELECTED_LANGUAGE, value).apply()

    var themeMode: String
        get() = prefs.getString(KEY_THEME_MODE, "system") ?: "system"
        set(value) = prefs.edit().putString(KEY_THEME_MODE, value).apply()

    var lastSyncStatus: String
        get() = prefs.getString(KEY_LAST_SYNC_STATUS, "Bundled Assets Ready") ?: "Bundled Assets Ready"
        set(value) = prefs.edit().putString(KEY_LAST_SYNC_STATUS, value).apply()

    val localVersionFlow: Flow<String> = callbackFlow {
        val listener = SharedPreferences.OnSharedPreferenceChangeListener { _, key ->
            if (key == KEY_LOCAL_VERSION) {
                trySend(localVersion)
            }
        }
        prefs.registerOnSharedPreferenceChangeListener(listener)
        trySend(localVersion)
        awaitClose { prefs.unregisterOnSharedPreferenceChangeListener(listener) }
    }
}

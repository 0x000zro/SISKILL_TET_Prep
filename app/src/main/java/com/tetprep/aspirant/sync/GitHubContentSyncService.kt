package com.tetprep.aspirant.sync

import android.content.Context
import android.util.Log
import androidx.room.withTransaction
import com.tetprep.aspirant.data.local.AppDatabase
import com.tetprep.aspirant.data.local.AppPreferencesRepository
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.data.local.entity.SubjectEntity
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import com.tetprep.aspirant.data.local.entity.TopicEntity
import com.tetprep.aspirant.data.model.MasterManifest
import com.tetprep.aspirant.data.model.MicroContentJson
import com.tetprep.aspirant.data.model.SubjectManifest
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit

sealed class SyncResult {
    data class Success(val newVersion: String, val message: String) : SyncResult()
    data class AlreadyUpToDate(val currentVersion: String) : SyncResult()
    data class Failure(val error: String) : SyncResult()
}

class GitHubContentSyncService(
    private val context: Context,
    private val database: AppDatabase,
    private val preferences: AppPreferencesRepository
) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .build()

    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = true
    }

    @Volatile
    private var lastErrorReason: String = "Unable to reach remote repository. Check internet connection."

    suspend fun syncContent(
        forceSync: Boolean = false,
        onProgress: (Int, String) -> Unit = { _, _ -> }
    ): SyncResult = withContext(Dispatchers.IO) {
        try {
            onProgress(5, "Connecting to GitHub repository...")
            var effectiveBasePath = Constants.REMOTE_CONTENT_BASE_PATH
            var masterJson = fetchFromRemoteWithFallback("$effectiveBasePath/master_manifest.json")

            if (masterJson == null) {
                val fallbackPath = Constants.REMOTE_CONTENT_FALLBACK_PATH
                masterJson = fetchFromRemoteWithFallback("$fallbackPath/master_manifest.json")
                if (masterJson != null) {
                    effectiveBasePath = fallbackPath
                } else {
                    return@withContext SyncResult.Failure(lastErrorReason)
                }
            }

            onProgress(15, "Verifying manifest version...")
            val remoteManifest = json.decodeFromString<MasterManifest>(masterJson)
            val currentVersion = preferences.localVersion

            if (!forceSync && !isRemoteVersionNewer(remoteManifest.version, currentVersion)) {
                preferences.lastSyncTimestamp = System.currentTimeMillis()
                preferences.lastSyncStatus = "Up to date ($currentVersion)"
                onProgress(100, "Content is already up to date.")
                return@withContext SyncResult.AlreadyUpToDate(currentVersion)
            }

            Log.i(TAG, "Sync active: Remote=${remoteManifest.version}, Local=$currentVersion, Force=$forceSync. Starting sync.")
            onProgress(25, "Synchronizing content (${remoteManifest.version})...")

            val subjectEntities = mutableListOf<SubjectEntity>()
            val topicEntities = mutableListOf<TopicEntity>()
            val subtopicEntities = mutableListOf<SubtopicEntity>()
            val microTopicEntities = mutableListOf<MicroTopicEntity>()
            val questionEntities = mutableListOf<QuestionEntity>()

            val subjectsCount = remoteManifest.subjects.size
            remoteManifest.subjects.forEachIndexed { sIdx, subjectItem ->
                val stepProgress = 25 + ((sIdx + 1) * 50 / subjectsCount.coerceAtLeast(1))
                onProgress(stepProgress, "Syncing ${subjectItem.nameEn}...")

                subjectEntities.add(
                    SubjectEntity(
                        id = subjectItem.id,
                        nameEn = subjectItem.nameEn,
                        nameHi = subjectItem.nameHi,
                        directory = subjectItem.directory,
                        manifestPath = subjectItem.manifestPath,
                        status = subjectItem.status,
                        totalTopics = subjectItem.totalTopics,
                        frameworkVersion = subjectItem.frameworkVersion,
                        taxonomyVersion = subjectItem.taxonomyVersion
                    )
                )

                // Fetch subject manifest
                val subjectPath = "$effectiveBasePath/${subjectItem.manifestPath}"
                val subjectJson = fetchFromRemoteWithFallback(subjectPath)
                if (subjectJson != null) {
                    try {
                        val parsedSubject = json.decodeFromString<SubjectManifest>(subjectJson)
                        parsedSubject.topics.forEachIndexed { tIdx, topicModel ->
                            val topicId = "${subjectItem.id}_${topicModel.id}"
                            val topicSlug = topicModel.slug ?: topicModel.code ?: "Topic_${topicModel.id}"
                            val topicTitleHi = topicModel.titleHi ?: topicModel.nameHi ?: topicSlug
                            val topicFolder = topicModel.folder ?: "Topic_${topicModel.id}_$topicSlug"

                            topicEntities.add(
                                TopicEntity(
                                    id = topicId,
                                    subjectId = subjectItem.id,
                                    code = topicModel.code ?: topicModel.id,
                                    slug = topicSlug,
                                    titleHi = topicTitleHi,
                                    orderNum = topicModel.order ?: (tIdx + 1),
                                    folder = topicFolder
                                )
                            )

                            topicModel.subtopics.forEachIndexed { stIdx, subtopicModel ->
                                val subtopicId = "${topicId}_${subtopicModel.id}"
                                val subtopicSlug = subtopicModel.slug ?: subtopicModel.code ?: "Subtopic_${subtopicModel.id}"
                                val subtopicTitleHi = subtopicModel.titleHi ?: subtopicModel.nameHi ?: subtopicSlug
                                val subtopicFolder = subtopicModel.folder ?: "Subtopic_${subtopicModel.id}_$subtopicSlug"

                                subtopicEntities.add(
                                    SubtopicEntity(
                                        id = subtopicId,
                                        topicId = topicId,
                                        subjectId = subjectItem.id,
                                        code = subtopicModel.code ?: subtopicModel.id,
                                        slug = subtopicSlug,
                                        titleHi = subtopicTitleHi,
                                        orderNum = subtopicModel.order ?: (stIdx + 1),
                                        folder = subtopicFolder
                                    )
                                )

                                subtopicModel.microTopics.forEachIndexed { mIdx, microModel ->
                                    val microIdVal = microModel.microId ?: microModel.id ?: "M01"
                                    val microUniqueId = "${subtopicId}_$microIdVal"
                                    val microSlug = microModel.slug ?: microIdVal
                                    val microNameHi = microModel.nameHi ?: microSlug
                                    val microFolder = microModel.folder ?: "Micro_${mIdx + 1}_$microSlug"

                                    val basePath = "$effectiveBasePath/${subjectItem.directory}/$topicFolder/$subtopicFolder/$microFolder"
                                    val localAssetBasePath = "${Constants.ASSETS_BUNDLED_PATH}/${subjectItem.directory}/$topicFolder/$subtopicFolder/$microFolder"
                                    val assetsList = if (microModel.assets.isNotEmpty()) microModel.assets else listOf("Concept", "Short_Notes", "MCQ", "PYQ", "Practice")
                                    val assetsJsonStr = json.encodeToString(assetsList)

                                    microTopicEntities.add(
                                        MicroTopicEntity(
                                            id = microUniqueId,
                                            subtopicId = subtopicId,
                                            subjectId = subjectItem.id,
                                            microId = microIdVal,
                                            code = microSlug,
                                            nameHi = microNameHi,
                                            folder = microFolder,
                                            orderNum = microModel.order ?: (mIdx + 1),
                                            assetsJson = assetsJsonStr,
                                            conceptPath = "$localAssetBasePath/Concept/content.md",
                                            shortNotesPath = "$localAssetBasePath/Short_Notes/content.md",
                                            practicePath = "$localAssetBasePath/Practice/content.md",
                                            mcqPath = "$localAssetBasePath/MCQ/content.json",
                                            pyqPath = "$localAssetBasePath/PYQ/content.json"
                                        )
                                    )

                                    // Fetch MCQ content.json if updated
                                    val mcqRemotePath = "$basePath/MCQ/content.json"
                                    fetchFromRemoteWithFallback(mcqRemotePath)?.let { mcqStr ->
                                        try {
                                            val mcqData = json.decodeFromString<MicroContentJson>(mcqStr)
                                            mcqData.questions.forEach { q ->
                                                questionEntities.add(
                                                    QuestionEntity(
                                                        id = q.id,
                                                        microTopicId = microUniqueId,
                                                        subjectId = subjectItem.id,
                                                        type = "MCQ",
                                                        question = q.question,
                                                        optionA = q.options.A,
                                                        optionB = q.options.B,
                                                        optionC = q.options.C,
                                                        optionD = q.options.D,
                                                        answer = q.answer,
                                                        explanation = q.explanation,
                                                        examTag = q.examTag,
                                                        bloomTaxonomyLevel = q.bloomTaxonomyLevel,
                                                        year = q.year
                                                    )
                                                )
                                            }
                                        } catch (e: Exception) {
                                            Log.w(TAG, "Error parsing remote MCQ for $microUniqueId", e)
                                        }
                                    }

                                    // Fetch PYQ content.json if updated
                                    val pyqRemotePath = "$basePath/PYQ/content.json"
                                    fetchFromRemoteWithFallback(pyqRemotePath)?.let { pyqStr ->
                                        try {
                                            val pyqData = json.decodeFromString<MicroContentJson>(pyqStr)
                                            pyqData.questions.forEach { q ->
                                                questionEntities.add(
                                                    QuestionEntity(
                                                        id = q.id,
                                                        microTopicId = microUniqueId,
                                                        subjectId = subjectItem.id,
                                                        type = "PYQ",
                                                        question = q.question,
                                                        optionA = q.options.A,
                                                        optionB = q.options.B,
                                                        optionC = q.options.C,
                                                        optionD = q.options.D,
                                                        answer = q.answer,
                                                        explanation = q.explanation,
                                                        examTag = q.examTag,
                                                        bloomTaxonomyLevel = q.bloomTaxonomyLevel,
                                                        year = q.year
                                                    )
                                                )
                                            }
                                        } catch (e: Exception) {
                                            Log.w(TAG, "Error parsing remote PYQ for $microUniqueId", e)
                                        }
                                    }

                                    // Fetch Markdown assets (Concept, Short_Notes, Practice) for offline caching
                                    listOf("Concept", "Short_Notes", "Practice").forEach { assetType ->
                                        val mdRemotePath = "$basePath/$assetType/content.md"
                                        fetchFromRemoteWithFallback(mdRemotePath)?.let { mdStr ->
                                            try {
                                                val localMdFile = File(context.filesDir, "$localAssetBasePath/$assetType/content.md")
                                                localMdFile.parentFile?.mkdirs()
                                                localMdFile.writeText(mdStr, Charsets.UTF_8)
                                            } catch (e: Exception) {
                                                Log.w(TAG, "Error caching $mdRemotePath to local storage", e)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } catch (e: Exception) {
                        Log.e(TAG, "Error parsing subject manifest $subjectPath", e)
                    }
                }
            }

            onProgress(85, "Applying database updates atomically...")
            database.withTransaction {
                database.subjectDao().insertSubjects(subjectEntities)
                database.topicDao().insertTopics(topicEntities)
                database.subtopicDao().insertSubtopics(subtopicEntities)
                database.microTopicDao().insertMicroTopics(microTopicEntities)
                if (questionEntities.isNotEmpty()) {
                    database.questionDao().insertQuestions(questionEntities)
                }
            }

            preferences.localVersion = remoteManifest.version
            preferences.lastSyncTimestamp = System.currentTimeMillis()
            preferences.lastSyncStatus = "Updated to ${remoteManifest.version}"

            onProgress(100, "Successfully updated to ${remoteManifest.version}!")
            SyncResult.Success(remoteManifest.version, "Sync complete. All subjects up to date.")
        } catch (e: Exception) {
            Log.e(TAG, "Sync process failed", e)
            SyncResult.Failure("Sync error: ${e.localizedMessage ?: "Unknown network failure"}")
        }
    }

    private fun fetchFromRemoteWithFallback(relativePath: String): String? {
        val rawUrl = "${Constants.getRawGitHubBaseUrl()}$relativePath"
        val rawResponse = executeHttpGet(rawUrl)
        if (rawResponse != null) {
            return rawResponse
        }

        // Fallback to jsDelivr CDN
        val cdnUrl = "${Constants.getCdnFallbackBaseUrl()}$relativePath"
        Log.d(TAG, "Falling back to CDN for: $cdnUrl")
        return executeHttpGet(cdnUrl)
    }

    private fun executeHttpGet(url: String): String? {
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "SISKILL-TET-Android-Client/1.0")
            .build()
        return try {
            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    response.body?.string()
                } else {
                    Log.w(TAG, "HTTP ${response.code} for $url")
                    val explanation = when (response.code) {
                        404 -> "HTTP 404: Repository or file not found.\n\nMake sure the GitHub repository '${Constants.DEFAULT_GITHUB_REPO}' is Public and pushed to branch '${Constants.DEFAULT_GITHUB_BRANCH}'."
                        403 -> "HTTP 403: Forbidden.\n\nIf the GitHub repository is set to Private, change visibility to Public in GitHub repository settings."
                        else -> "HTTP ${response.code} received from GitHub."
                    }
                    lastErrorReason = "$explanation\n\nAttempted URL:\n$url"
                    null
                }
            }
        } catch (e: IOException) {
            Log.w(TAG, "Connection failed for $url: ${e.message}")
            lastErrorReason = "Connection failed: ${e.localizedMessage ?: e.message ?: "Network unreachable"}\n\nAttempted URL:\n$url"
            null
        }
    }

    private fun isRemoteVersionNewer(remoteVersion: String, localVersion: String): Boolean {
        if (localVersion == "0.0.0") return true
        val rParts = remoteVersion.split(".").mapNotNull { it.toIntOrNull() }
        val lParts = localVersion.split(".").mapNotNull { it.toIntOrNull() }
        for (i in 0 until minOf(rParts.size, lParts.size)) {
            if (rParts[i] > lParts[i]) return true
            if (rParts[i] < lParts[i]) return false
        }
        return rParts.size > lParts.size
    }

    companion object {
        private const val TAG = "GitHubContentSync"
    }
}

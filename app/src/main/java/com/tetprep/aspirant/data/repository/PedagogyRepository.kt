package com.tetprep.aspirant.data.repository

import android.content.Context
import com.tetprep.aspirant.data.local.AppDatabase
import com.tetprep.aspirant.data.local.AppPreferencesRepository
import com.tetprep.aspirant.data.local.entity.BookmarkEntity
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import com.tetprep.aspirant.data.local.entity.MockTestEntity
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.data.local.entity.SubjectEntity
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import com.tetprep.aspirant.data.local.entity.TopicEntity
import com.tetprep.aspirant.data.local.entity.UserProgressEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.withContext
import java.io.InputStreamReader

class PedagogyRepository(
    private val context: Context,
    private val database: AppDatabase,
    val preferences: AppPreferencesRepository
) {
    // Subjects
    fun getAllSubjects(): Flow<List<SubjectEntity>> =
        database.subjectDao().getAllSubjects()

    fun getSubjectById(id: String): Flow<SubjectEntity?> =
        database.subjectDao().getSubjectById(id)

    // Topics & Hierarchy
    fun getTopicsBySubject(subjectId: String): Flow<List<TopicEntity>> =
        database.topicDao().getTopicsBySubject(subjectId)

    fun getSubtopicsByTopic(topicId: String): Flow<List<SubtopicEntity>> =
        database.subtopicDao().getSubtopicsByTopic(topicId)

    fun getMicroTopicsBySubtopic(subtopicId: String): Flow<List<MicroTopicEntity>> =
        database.microTopicDao().getMicroTopicsBySubtopic(subtopicId)

    fun getMicroTopicById(id: String): Flow<MicroTopicEntity?> =
        database.microTopicDao().getMicroTopicById(id)

    suspend fun getMicroTopicByIdDirect(id: String): MicroTopicEntity? =
        database.microTopicDao().getMicroTopicByIdDirect(id)

    // Questions
    fun getQuestionsByMicroTopicAndType(microTopicId: String, type: String): Flow<List<QuestionEntity>> =
        database.questionDao().getQuestionsByMicroTopicAndType(microTopicId, type)

    fun getRandomPracticeQuestions(subjectId: String, type: String, limit: Int = 30): Flow<List<QuestionEntity>> =
        database.questionDao().getRandomQuestionsBySubject(subjectId, type, limit)

    // Progress
    fun getProgress(microTopicId: String, assetType: String): Flow<UserProgressEntity?> =
        database.userProgressDao().getProgress(microTopicId, assetType)

    fun getCompletedMicroTopicCount(): Flow<Int> =
        database.userProgressDao().getCompletedMicroTopicCount()

    fun getTotalQuizScore(): Flow<Int?> =
        database.userProgressDao().getTotalQuizScore()

    fun getTotalAttemptedQuestions(): Flow<Int?> =
        database.userProgressDao().getTotalAttemptedQuestions()

    suspend fun saveProgress(
        microTopicId: String,
        assetType: String,
        isCompleted: Boolean,
        score: Int = 0,
        totalQuestions: Int = 0
    ) = withContext(Dispatchers.IO) {
        val entity = UserProgressEntity(
            id = "${microTopicId}_$assetType",
            microTopicId = microTopicId,
            assetType = assetType,
            isCompleted = isCompleted,
            score = score,
            totalQuestions = totalQuestions,
            lastAccessedTime = System.currentTimeMillis()
        )
        database.userProgressDao().upsertProgress(entity)
    }

    // Bookmarks
    fun getAllBookmarks(): Flow<List<BookmarkEntity>> =
        database.bookmarkDao().getAllBookmarks()

    fun isBookmarked(questionId: String): Flow<Boolean> =
        database.bookmarkDao().isBookmarked(questionId)

    suspend fun toggleBookmark(question: QuestionEntity) = withContext(Dispatchers.IO) {
        val already = database.bookmarkDao().isBookmarkedDirect(question.id)
        if (already) {
            database.bookmarkDao().deleteBookmark(question.id)
        } else {
            val bookmark = BookmarkEntity(
                id = question.id,
                questionId = question.id,
                microTopicId = question.microTopicId,
                title = "Q: ${question.examTag}",
                snippet = question.question.take(120),
                createdAt = System.currentTimeMillis()
            )
            database.bookmarkDao().insertBookmark(bookmark)
        }
    }

    suspend fun deleteBookmark(questionId: String) = withContext(Dispatchers.IO) {
        database.bookmarkDao().deleteBookmark(questionId)
    }

    // Mock Tests
    fun getAllMockTests(): Flow<List<MockTestEntity>> =
        database.mockTestDao().getAllMockTests()

    fun getMockTestById(testId: String): Flow<MockTestEntity?> =
        database.mockTestDao().getMockTestById(testId)

    suspend fun getMockTestByIdDirect(testId: String): MockTestEntity? =
        database.mockTestDao().getMockTestByIdDirect(testId)

    // Markdown file reader with local asset fallback
    suspend fun readMarkdownContent(assetPath: String?): String = withContext(Dispatchers.IO) {
        if (assetPath == null) return@withContext "*No content specified.*"
        try {
            context.assets.open(assetPath).use { inputStream ->
                InputStreamReader(inputStream, Charsets.UTF_8).use { reader ->
                    reader.readText()
                }
            }
        } catch (e: Exception) {
            "*Content is being compiled. Please check for updates.*"
        }
    }
}

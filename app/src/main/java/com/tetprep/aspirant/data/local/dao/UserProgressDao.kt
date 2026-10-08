package com.tetprep.aspirant.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.tetprep.aspirant.data.local.entity.UserProgressEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface UserProgressDao {
    @Query("SELECT * FROM user_progress WHERE microTopicId = :microTopicId AND assetType = :assetType LIMIT 1")
    fun getProgress(microTopicId: String, assetType: String): Flow<UserProgressEntity?>

    @Query("SELECT * FROM user_progress")
    fun getAllProgress(): Flow<List<UserProgressEntity>>

    @Query("SELECT COUNT(DISTINCT microTopicId) FROM user_progress WHERE isCompleted = 1")
    fun getCompletedMicroTopicCount(): Flow<Int>

    @Query("SELECT SUM(score) FROM user_progress WHERE assetType IN ('MCQ', 'PYQ')")
    fun getTotalQuizScore(): Flow<Int?>

    @Query("SELECT SUM(totalQuestions) FROM user_progress WHERE assetType IN ('MCQ', 'PYQ')")
    fun getTotalAttemptedQuestions(): Flow<Int?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertProgress(progress: UserProgressEntity)
}

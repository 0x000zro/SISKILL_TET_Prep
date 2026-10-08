package com.tetprep.aspirant.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface QuestionDao {
    @Query("SELECT * FROM questions WHERE microTopicId = :microTopicId AND type = :type")
    fun getQuestionsByMicroTopicAndType(microTopicId: String, type: String): Flow<List<QuestionEntity>>

    @Query("SELECT * FROM questions WHERE microTopicId = :microTopicId AND type = :type")
    suspend fun getQuestionsByMicroTopicAndTypeDirect(microTopicId: String, type: String): List<QuestionEntity>

    @Query("SELECT * FROM questions WHERE subjectId = :subjectId AND type = :type ORDER BY RANDOM() LIMIT :limit")
    fun getRandomQuestionsBySubject(subjectId: String, type: String, limit: Int = 30): Flow<List<QuestionEntity>>

    @Query("SELECT * FROM questions WHERE type = :type ORDER BY RANDOM() LIMIT :limit")
    suspend fun getRandomQuestionsByTypeDirect(type: String, limit: Int = 30): List<QuestionEntity>

    @Query("SELECT * FROM questions WHERE id = :id LIMIT 1")
    fun getQuestionById(id: String): Flow<QuestionEntity?>

    @Query("SELECT * FROM questions WHERE id = :id LIMIT 1")
    suspend fun getQuestionByIdDirect(id: String): QuestionEntity?

    @Query("SELECT COUNT(*) FROM questions")
    suspend fun countQuestions(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertQuestions(questions: List<QuestionEntity>)
}

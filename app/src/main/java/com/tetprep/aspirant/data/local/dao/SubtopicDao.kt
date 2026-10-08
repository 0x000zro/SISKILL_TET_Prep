package com.tetprep.aspirant.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface SubtopicDao {
    @Query("SELECT * FROM subtopics WHERE topicId = :topicId ORDER BY orderNum ASC, id ASC")
    fun getSubtopicsByTopic(topicId: String): Flow<List<SubtopicEntity>>

    @Query("SELECT * FROM subtopics WHERE topicId = :topicId ORDER BY orderNum ASC, id ASC")
    suspend fun getSubtopicsByTopicDirect(topicId: String): List<SubtopicEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSubtopics(subtopics: List<SubtopicEntity>)
}

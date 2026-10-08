package com.tetprep.aspirant.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface MicroTopicDao {
    @Query("SELECT * FROM micro_topics WHERE subtopicId = :subtopicId ORDER BY orderNum ASC, id ASC")
    fun getMicroTopicsBySubtopic(subtopicId: String): Flow<List<MicroTopicEntity>>

    @Query("SELECT * FROM micro_topics WHERE subtopicId = :subtopicId ORDER BY orderNum ASC, id ASC")
    suspend fun getMicroTopicsBySubtopicDirect(subtopicId: String): List<MicroTopicEntity>

    @Query("SELECT * FROM micro_topics WHERE id = :id LIMIT 1")
    fun getMicroTopicById(id: String): Flow<MicroTopicEntity?>

    @Query("SELECT * FROM micro_topics WHERE id = :id LIMIT 1")
    suspend fun getMicroTopicByIdDirect(id: String): MicroTopicEntity?

    @Query("SELECT COUNT(*) FROM micro_topics")
    suspend fun countMicroTopics(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMicroTopics(microTopics: List<MicroTopicEntity>)
}

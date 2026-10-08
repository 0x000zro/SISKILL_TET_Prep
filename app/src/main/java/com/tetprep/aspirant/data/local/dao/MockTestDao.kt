package com.tetprep.aspirant.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.tetprep.aspirant.data.local.entity.MockTestEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface MockTestDao {
    @Query("SELECT * FROM mock_tests")
    fun getAllMockTests(): Flow<List<MockTestEntity>>

    @Query("SELECT * FROM mock_tests WHERE testId = :testId LIMIT 1")
    fun getMockTestById(testId: String): Flow<MockTestEntity?>

    @Query("SELECT * FROM mock_tests WHERE testId = :testId LIMIT 1")
    suspend fun getMockTestByIdDirect(testId: String): MockTestEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMockTests(tests: List<MockTestEntity>)
}

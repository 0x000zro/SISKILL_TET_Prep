package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "mock_tests")
data class MockTestEntity(
    @PrimaryKey
    val testId: String,
    val title: String,
    val paperCode: String = "Paper_1",
    val durationMinutes: Int = 150,
    val totalMarks: Int = 150,
    val negativeMarkingRate: Double = 0.0,
    val sectionsJson: String
)

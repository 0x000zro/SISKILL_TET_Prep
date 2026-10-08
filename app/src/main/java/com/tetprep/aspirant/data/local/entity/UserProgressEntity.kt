package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "user_progress",
    indices = [
        Index(value = ["microTopicId", "assetType"], unique = true)
    ]
)
data class UserProgressEntity(
    @PrimaryKey
    val id: String, // "${microTopicId}_${assetType}"
    val microTopicId: String,
    val assetType: String, // "Concept", "Short_Notes", "MCQ", "PYQ", "Practice"
    val isCompleted: Boolean = false,
    val score: Int = 0,
    val totalQuestions: Int = 0,
    val lastAccessedTime: Long = System.currentTimeMillis()
)

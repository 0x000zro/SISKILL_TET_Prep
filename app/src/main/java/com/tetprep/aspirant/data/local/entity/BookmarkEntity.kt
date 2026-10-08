package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "bookmarks",
    indices = [
        Index(value = ["questionId"], unique = true)
    ]
)
data class BookmarkEntity(
    @PrimaryKey
    val id: String, // questionId
    val questionId: String,
    val microTopicId: String,
    val title: String,
    val snippet: String,
    val createdAt: Long = System.currentTimeMillis()
)

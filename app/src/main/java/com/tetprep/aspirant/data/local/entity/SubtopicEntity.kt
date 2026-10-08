package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "subtopics",
    foreignKeys = [
        ForeignKey(
            entity = TopicEntity::class,
            parentColumns = ["id"],
            childColumns = ["topicId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index(value = ["topicId"])]
)
data class SubtopicEntity(
    @PrimaryKey
    val id: String, // e.g. "CDP_T01_ST01"
    val topicId: String,
    val subjectId: String,
    val code: String,
    val slug: String,
    val titleHi: String,
    val orderNum: Int,
    val folder: String
)

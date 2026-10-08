package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "topics",
    foreignKeys = [
        ForeignKey(
            entity = SubjectEntity::class,
            parentColumns = ["id"],
            childColumns = ["subjectId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index(value = ["subjectId"])]
)
data class TopicEntity(
    @PrimaryKey
    val id: String, // e.g. "CDP_T01" or "T01"
    val subjectId: String,
    val code: String,
    val slug: String,
    val titleHi: String,
    val orderNum: Int,
    val folder: String
)

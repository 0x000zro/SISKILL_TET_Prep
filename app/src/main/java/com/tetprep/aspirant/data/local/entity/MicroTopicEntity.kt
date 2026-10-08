package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "micro_topics",
    foreignKeys = [
        ForeignKey(
            entity = SubtopicEntity::class,
            parentColumns = ["id"],
            childColumns = ["subtopicId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [
        Index(value = ["subtopicId"]),
        Index(value = ["microId"])
    ]
)
data class MicroTopicEntity(
    @PrimaryKey
    val id: String, // e.g. "CDP_T01_ST01_M01" or "ST01_01_M01"
    val subtopicId: String,
    val subjectId: String,
    val microId: String,
    val code: String,
    val nameHi: String,
    val folder: String,
    val orderNum: Int,
    val assetsJson: String, // '["Concept","Short_Notes","PYQ","MCQ","Practice"]'
    val conceptPath: String? = null,
    val shortNotesPath: String? = null,
    val practicePath: String? = null,
    val mcqPath: String? = null,
    val pyqPath: String? = null
)

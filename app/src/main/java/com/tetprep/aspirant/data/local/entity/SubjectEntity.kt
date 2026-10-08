package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "subjects")
data class SubjectEntity(
    @PrimaryKey
    val id: String, // e.g. "CDP", "HINDI", "MATH", "EVS", "ENG", "SAN"
    val nameEn: String,
    val nameHi: String,
    val directory: String,
    val manifestPath: String,
    val status: String,
    val totalTopics: Int,
    val frameworkVersion: String? = "1.0.0",
    val taxonomyVersion: String? = "1.0.0"
)

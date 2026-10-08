package com.tetprep.aspirant.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "questions",
    indices = [
        Index(value = ["microTopicId"]),
        Index(value = ["type"]),
        Index(value = ["subjectId"])
    ]
)
data class QuestionEntity(
    @PrimaryKey
    val id: String,
    val microTopicId: String,
    val subjectId: String,
    val type: String, // "MCQ", "PYQ", "MOCK"
    val question: String,
    val optionA: String,
    val optionB: String,
    val optionC: String,
    val optionD: String,
    val answer: String, // "A", "B", "C", "D"
    val explanation: String,
    val examTag: String,
    val bloomTaxonomyLevel: String? = null,
    val year: String? = null
)

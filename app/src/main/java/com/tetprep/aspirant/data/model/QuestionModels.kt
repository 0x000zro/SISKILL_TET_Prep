package com.tetprep.aspirant.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class MicroContentJson(
    @SerialName("micro_topic_id")
    val microTopicId: String? = null,
    val type: String? = null,
    @SerialName("total_questions")
    val totalQuestions: Int = 0,
    val questions: List<QuestionJsonModel> = emptyList()
)

@Serializable
data class QuestionJsonModel(
    val id: String = "",
    val question: String = "",
    val options: OptionsJsonModel = OptionsJsonModel(),
    val answer: String = "A",
    val explanation: String = "",
    @SerialName("exam_tag")
    val examTag: String = "UPTET / CTET",
    @SerialName("bloom_taxonomy_level")
    val bloomTaxonomyLevel: String? = null,
    val year: String? = null
)

@Serializable
data class OptionsJsonModel(
    val A: String = "",
    val B: String = "",
    val C: String = "",
    val D: String = ""
)

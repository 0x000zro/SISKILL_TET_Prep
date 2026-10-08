package com.tetprep.aspirant.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ExamDefinitionModel(
    @SerialName("exam_code")
    val examCode: String,
    @SerialName("title_en")
    val titleEn: String,
    @SerialName("title_hi")
    val titleHi: String,
    @SerialName("conducting_body")
    val conductingBody: String,
    @SerialName("validity_years")
    val validityYears: String? = "Lifetime",
    @SerialName("negative_marking")
    val negativeMarking: Boolean = false,
    @SerialName("applicable_papers")
    val applicablePapers: List<String> = emptyList()
)

@Serializable
data class PaperDefinitionModel(
    @SerialName("paper_code")
    val paperCode: String,
    @SerialName("target_classes")
    val targetClasses: String,
    @SerialName("duration_minutes")
    val durationMinutes: Int = 150,
    @SerialName("total_marks")
    val totalMarks: Int = 150,
    @SerialName("total_questions")
    val totalQuestions: Int = 150,
    @SerialName("qualifying_percentage")
    val qualifyingPercentage: QualifyingPercentageModel? = null
)

@Serializable
data class QualifyingPercentageModel(
    val general: Double = 60.0,
    val reserved: Double = 55.0
)

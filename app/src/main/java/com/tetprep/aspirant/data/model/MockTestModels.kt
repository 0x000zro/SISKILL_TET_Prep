package com.tetprep.aspirant.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class MockTestPaperModel(
    @SerialName("test_id")
    val testId: String,
    val title: String,
    @SerialName("paper_code")
    val paperCode: String = "Paper_1",
    @SerialName("duration_minutes")
    val durationMinutes: Int = 150,
    @SerialName("total_marks")
    val totalMarks: Int = 150,
    @SerialName("negative_marking_rate")
    val negativeMarkingRate: Double = 0.0,
    val sections: List<SectionJsonModel> = emptyList()
)

@Serializable
data class SectionJsonModel(
    @SerialName("section_name")
    val sectionName: String,
    @SerialName("subject_id")
    val subjectId: String,
    @SerialName("question_count")
    val questionCount: Int,
    val questions: List<QuestionJsonModel> = emptyList()
)

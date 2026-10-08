package com.tetprep.aspirant.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class MasterManifest(
    val exam: String = "UPTET_CTET",
    val paper: String = "Paper_1_and_2",
    val version: String = "1.0.0",
    @SerialName("active_subjects_count")
    val activeSubjectsCount: Int = 6,
    @SerialName("total_planned_subjects")
    val totalPlannedSubjects: Int = 6,
    val subjects: List<SubjectManifestItem> = emptyList(),
    val brand: String? = null,
    val tagline: String? = null,
    @SerialName("official_domain")
    val officialDomain: String? = null,
    @SerialName("support_email")
    val supportEmail: String? = null,
    @SerialName("package_name")
    val packageName: String? = null
)

@Serializable
data class SubjectManifestItem(
    val id: String,
    @SerialName("name_en")
    val nameEn: String,
    @SerialName("name_hi")
    val nameHi: String,
    val directory: String,
    @SerialName("manifest_path")
    val manifestPath: String,
    val status: String = "scaffolded",
    @SerialName("total_topics")
    val totalTopics: Int = 0,
    @SerialName("framework_version")
    val frameworkVersion: String? = "1.0.0",
    @SerialName("taxonomy_version")
    val taxonomyVersion: String? = "1.0.0"
)

@Serializable
data class SubjectManifest(
    @SerialName("schema_version")
    val schemaVersion: String? = null,
    @SerialName("framework_version")
    val frameworkVersion: String? = null,
    @SerialName("content_version")
    val contentVersion: String? = null,
    @SerialName("taxonomy_version")
    val taxonomyVersion: String? = null,
    val status: String? = null,
    val subject: SubjectDetail? = null,
    @SerialName("name_en")
    val nameEn: String? = null,
    @SerialName("name_hi")
    val nameHi: String? = null,
    @SerialName("total_topics")
    val totalTopics: Int? = null,
    @SerialName("asset_types")
    val assetTypes: List<String> = emptyList(),
    val topics: List<TopicJsonModel> = emptyList()
)

@Serializable
data class SubjectDetail(
    val id: String,
    val type: String? = null,
    @SerialName("name_en")
    val nameEn: String,
    @SerialName("name_hi")
    val nameHi: String,
    val directory: String? = null
)

@Serializable
data class TopicJsonModel(
    val id: String,
    val slug: String? = null,
    val code: String? = null,
    @SerialName("title_hi")
    val titleHi: String? = null,
    @SerialName("name_hi")
    val nameHi: String? = null,
    val order: Int? = null,
    val folder: String? = null,
    val subtopics: List<SubtopicJsonModel> = emptyList()
)

@Serializable
data class SubtopicJsonModel(
    val id: String,
    val slug: String? = null,
    val code: String? = null,
    @SerialName("title_hi")
    val titleHi: String? = null,
    @SerialName("name_hi")
    val nameHi: String? = null,
    val order: Int? = null,
    val folder: String? = null,
    @SerialName("micro_topics")
    val microTopics: List<MicroTopicJsonModel> = emptyList()
)

@Serializable
data class MicroTopicJsonModel(
    val id: String? = null,
    @SerialName("micro_id")
    val microId: String? = null,
    val slug: String? = null,
    val folder: String? = null,
    @SerialName("name_hi")
    val nameHi: String? = null,
    val order: Int? = null,
    val assets: List<String> = emptyList()
)

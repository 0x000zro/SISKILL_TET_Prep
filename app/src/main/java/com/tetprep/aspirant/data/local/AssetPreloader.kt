package com.tetprep.aspirant.data.local

import android.content.Context
import android.util.Log
import com.tetprep.aspirant.data.local.entity.MicroTopicEntity
import com.tetprep.aspirant.data.local.entity.MockTestEntity
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import com.tetprep.aspirant.data.local.entity.SubjectEntity
import com.tetprep.aspirant.data.local.entity.SubtopicEntity
import com.tetprep.aspirant.data.local.entity.TopicEntity
import com.tetprep.aspirant.data.model.MasterManifest
import com.tetprep.aspirant.data.model.MicroContentJson
import com.tetprep.aspirant.data.model.MockTestPaperModel
import com.tetprep.aspirant.data.model.OptionsJsonModel
import com.tetprep.aspirant.data.model.QuestionJsonModel
import com.tetprep.aspirant.data.model.SectionJsonModel
import com.tetprep.aspirant.data.model.SubjectManifest
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.io.InputStreamReader

class AssetPreloader(
    private val context: Context,
    private val database: AppDatabase,
    private val preferences: AppPreferencesRepository
) {
    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = true
    }

    suspend fun preloadIfNeeded(onProgress: (Int, String) -> Unit = { _, _ -> }): Boolean =
        withContext(Dispatchers.IO) {
            val subjectCount = database.subjectDao().countSubjects()
            if (preferences.isInitialized && subjectCount > 0) {
                Log.d(TAG, "Database already initialized with $subjectCount subjects.")
                return@withContext true
            }

            try {
                onProgress(10, "Loading master pedagogical manifest...")
                val masterJsonString = readAssetFile(Constants.ASSETS_MASTER_MANIFEST)
                    ?: run {
                        Log.e(TAG, "Failed to load master manifest from assets.")
                        return@withContext false
                    }

                val masterManifest = json.decodeFromString<MasterManifest>(masterJsonString)
                preferences.localVersion = masterManifest.version
                preferences.lastSyncTimestamp = System.currentTimeMillis()

                val subjectEntities = mutableListOf<SubjectEntity>()
                val topicEntities = mutableListOf<TopicEntity>()
                val subtopicEntities = mutableListOf<SubtopicEntity>()
                val microTopicEntities = mutableListOf<MicroTopicEntity>()
                val questionEntities = mutableListOf<QuestionEntity>()

                val totalSubjects = masterManifest.subjects.size
                masterManifest.subjects.forEachIndexed { index, subjectItem ->
                    val progressPercent = 10 + ((index + 1) * 70 / totalSubjects.coerceAtLeast(1))
                    onProgress(progressPercent, "Parsing ${subjectItem.nameEn}...")

                    subjectEntities.add(
                        SubjectEntity(
                            id = subjectItem.id,
                            nameEn = subjectItem.nameEn,
                            nameHi = subjectItem.nameHi,
                            directory = subjectItem.directory,
                            manifestPath = subjectItem.manifestPath,
                            status = subjectItem.status,
                            totalTopics = subjectItem.totalTopics,
                            frameworkVersion = subjectItem.frameworkVersion,
                            taxonomyVersion = subjectItem.taxonomyVersion
                        )
                    )

                    // Read subject manifest
                    val subjectManifestPath = "${Constants.ASSETS_BUNDLED_PATH}/${subjectItem.manifestPath}"
                    val subjectJsonString = readAssetFile(subjectManifestPath)
                    if (subjectJsonString != null) {
                        try {
                            val subjectManifest = json.decodeFromString<SubjectManifest>(subjectJsonString)
                            subjectManifest.topics.forEachIndexed { tIdx, topicModel ->
                                val topicId = "${subjectItem.id}_${topicModel.id}"
                                val topicSlug = topicModel.slug ?: topicModel.code ?: "Topic_${topicModel.id}"
                                val topicTitleHi = topicModel.titleHi ?: topicModel.nameHi ?: topicSlug
                                val topicFolder = topicModel.folder ?: "Topic_${topicModel.id}_$topicSlug"

                                topicEntities.add(
                                    TopicEntity(
                                        id = topicId,
                                        subjectId = subjectItem.id,
                                        code = topicModel.code ?: topicModel.id,
                                        slug = topicSlug,
                                        titleHi = topicTitleHi,
                                        orderNum = topicModel.order ?: (tIdx + 1),
                                        folder = topicFolder
                                    )
                                )

                                topicModel.subtopics.forEachIndexed { stIdx, subtopicModel ->
                                    val subtopicId = "${topicId}_${subtopicModel.id}"
                                    val subtopicSlug = subtopicModel.slug ?: subtopicModel.code ?: "Subtopic_${subtopicModel.id}"
                                    val subtopicTitleHi = subtopicModel.titleHi ?: subtopicModel.nameHi ?: subtopicSlug
                                    val subtopicFolder = subtopicModel.folder ?: "Subtopic_${subtopicModel.id}_$subtopicSlug"

                                    subtopicEntities.add(
                                        SubtopicEntity(
                                            id = subtopicId,
                                            topicId = topicId,
                                            subjectId = subjectItem.id,
                                            code = subtopicModel.code ?: subtopicModel.id,
                                            slug = subtopicSlug,
                                            titleHi = subtopicTitleHi,
                                            orderNum = subtopicModel.order ?: (stIdx + 1),
                                            folder = subtopicFolder
                                        )
                                    )

                                    subtopicModel.microTopics.forEachIndexed { mIdx, microModel ->
                                        val microIdVal = microModel.microId ?: microModel.id ?: "M01"
                                        val microUniqueId = "${subtopicId}_$microIdVal"
                                        val microSlug = microModel.slug ?: microIdVal
                                        val microNameHi = microModel.nameHi ?: microSlug
                                        val microFolder = microModel.folder ?: "Micro_${mIdx + 1}_$microSlug"

                                        val basePath = "${Constants.ASSETS_BUNDLED_PATH}/${subjectItem.directory}/$topicFolder/$subtopicFolder/$microFolder"

                                        val assetsList = if (microModel.assets.isNotEmpty()) microModel.assets else listOf("Concept", "Short_Notes", "MCQ", "PYQ", "Practice")
                                        val assetsJsonStr = json.encodeToString(assetsList)

                                        microTopicEntities.add(
                                            MicroTopicEntity(
                                                id = microUniqueId,
                                                subtopicId = subtopicId,
                                                subjectId = subjectItem.id,
                                                microId = microIdVal,
                                                code = microSlug,
                                                nameHi = microNameHi,
                                                folder = microFolder,
                                                orderNum = microModel.order ?: (mIdx + 1),
                                                assetsJson = assetsJsonStr,
                                                conceptPath = "$basePath/Concept/content.md",
                                                shortNotesPath = "$basePath/Short_Notes/content.md",
                                                practicePath = "$basePath/Practice/content.md",
                                                mcqPath = "$basePath/MCQ/content.json",
                                                pyqPath = "$basePath/PYQ/content.json"
                                            )
                                        )

                                        // Try reading bundled MCQ content.json
                                        readAssetFile("$basePath/MCQ/content.json")?.let { mcqStr ->
                                            try {
                                                val parsedQuestions = com.tetprep.aspirant.data.parser.PedagogyContentParser.parseQuestions(
                                                    jsonString = mcqStr,
                                                    microTopicId = microUniqueId,
                                                    subjectId = subjectItem.id,
                                                    defaultType = "MCQ"
                                                )
                                                questionEntities.addAll(parsedQuestions)
                                            } catch (e: Exception) {
                                                Log.w(TAG, "Error parsing bundled MCQ for $microUniqueId", e)
                                            }
                                        }

                                        // Try reading bundled PYQ content.json
                                        readAssetFile("$basePath/PYQ/content.json")?.let { pyqStr ->
                                            try {
                                                val parsedQuestions = com.tetprep.aspirant.data.parser.PedagogyContentParser.parseQuestions(
                                                    jsonString = pyqStr,
                                                    microTopicId = microUniqueId,
                                                    subjectId = subjectItem.id,
                                                    defaultType = "PYQ"
                                                )
                                                questionEntities.addAll(parsedQuestions)
                                            } catch (e: Exception) {
                                                Log.w(TAG, "Error parsing bundled PYQ for $microUniqueId", e)
                                            }
                                        }
                                    }
                                }
                            }
                        } catch (e: Exception) {
                            Log.e(TAG, "Error parsing subject manifest for ${subjectItem.id}", e)
                        }
                    }
                }

                onProgress(85, "Saving pedagogical hierarchy into Room database...")
                database.subjectDao().insertSubjects(subjectEntities)
                database.topicDao().insertTopics(topicEntities)
                database.subtopicDao().insertSubtopics(subtopicEntities)
                database.microTopicDao().insertMicroTopics(microTopicEntities)
                if (questionEntities.isNotEmpty()) {
                    database.questionDao().insertQuestions(questionEntities)
                }

                // Seed Mock Exam simulation matching schemas/mock.schema.json
                onProgress(95, "Generating CTET Paper 1 & 2 standard mock simulation...")
                seedDefaultMockTest()

                preferences.isInitialized = true
                preferences.lastSyncStatus = "Local assets preloaded successfully."
                onProgress(100, "Ready!")
                Log.i(TAG, "Preload completed successfully: ${subjectEntities.size} subjects, ${topicEntities.size} topics, ${microTopicEntities.size} micro-topics.")
                true
            } catch (e: Exception) {
                Log.e(TAG, "Preload failed with exception", e)
                false
            }
        }

    private suspend fun seedDefaultMockTest() {
        val sampleQuestions = listOf(
            QuestionJsonModel(
                id = "CDP_MOCK_Q01",
                question = "According to Jean Piaget, children's thinking differs from that of adults in _______ rather than in _______.",
                options = OptionsJsonModel(
                    A = "size; correctness",
                    B = "kind; amount",
                    C = "amount; kind",
                    D = "capacity; quantity"
                ),
                answer = "B",
                explanation = "Piaget proposed that children's cognitive structures differ qualitatively (in kind) from adults, rather than merely quantitatively (in amount).",
                examTag = "CTET Official Benchmark",
                bloomTaxonomyLevel = "Understanding"
            ),
            QuestionJsonModel(
                id = "CDP_MOCK_Q02",
                question = "The concept of 'Zone of Proximal Development' (ZPD) was introduced by:",
                options = OptionsJsonModel(
                    A = "Lev Vygotsky",
                    B = "Jean Piaget",
                    C = "Jerome Bruner",
                    D = "B.F. Skinner"
                ),
                answer = "A",
                explanation = "Lev Vygotsky defined ZPD as the distance between actual developmental level and potential level under adult guidance or peer collaboration.",
                examTag = "UPTET Benchmark",
                bloomTaxonomyLevel = "Remembering"
            ),
            QuestionJsonModel(
                id = "HINDI_MOCK_Q01",
                question = "प्राथमिक स्तर पर बच्चों की भाषा क्षमता का विकास करने का सबसे महत्वपूर्ण साधन क्या है?",
                options = OptionsJsonModel(
                    A = "साहित्यिक पुस्तकें पढ़ना",
                    B = "व्याकरण के नियमों का कंठस्थीकरण",
                    C = "समृद्ध भाषायी परिवेश और अभिव्यक्ति के अवसर",
                    D = "सुलेख और वर्तनी अभ्यास"
                ),
                answer = "C",
                explanation = "राष्ट्रीय पाठ्यचर्या रूपरेखा (NCF) के अनुसार समृद्ध भाषायी परिवेश में बच्चे स्वाभाविक रूप से भाषा अर्जित करते हैं।",
                examTag = "CTET Official",
                bloomTaxonomyLevel = "Applying"
            ),
            QuestionJsonModel(
                id = "MATH_MOCK_Q01",
                question = "According to George Polya, the main goal of mathematics education in schools is to:",
                options = OptionsJsonModel(
                    A = "Memorize multiplication tables and geometric formulae",
                    B = "Mathematize the child's thought processes and problem solving",
                    C = "Train students for competitive calculations only",
                    D = "Focus only on arithmetic algorithms"
                ),
                answer = "B",
                explanation = "George Polya emphasized mathematization of thinking rather than mechanical calculation.",
                examTag = "CTET Official",
                bloomTaxonomyLevel = "Understanding"
            ),
            QuestionJsonModel(
                id = "EVS_MOCK_Q01",
                question = "In the EVS curriculum, themes are designed to promote:",
                options = OptionsJsonModel(
                    A = "Rote memorization of scientific terminology",
                    B = "An integrated, experiential, and holistic perspective of the child's world",
                    C = "Disciplinary boundaries between physics, chemistry, and biology",
                    D = "Strict separation of environment and social realities"
                ),
                answer = "B",
                explanation = "NCF 2005 integrates EVS into 6 broad themes (Family & Friends, Food, Shelter, Water, Travel, Things We Make and Do) for experiential holistic learning.",
                examTag = "CTET Official",
                bloomTaxonomyLevel = "Evaluating"
            )
        )

        val sections = listOf(
            SectionJsonModel(
                sectionName = "Child Development & Pedagogy",
                subjectId = "CDP",
                questionCount = 30,
                questions = sampleQuestions.filter { it.id.startsWith("CDP") }
            ),
            SectionJsonModel(
                sectionName = "Hindi Language & Pedagogy",
                subjectId = "HINDI",
                questionCount = 30,
                questions = sampleQuestions.filter { it.id.startsWith("HINDI") }
            ),
            SectionJsonModel(
                sectionName = "Mathematics & Pedagogy",
                subjectId = "MATH",
                questionCount = 30,
                questions = sampleQuestions.filter { it.id.startsWith("MATH") }
            ),
            SectionJsonModel(
                sectionName = "Environmental Studies & Pedagogy",
                subjectId = "EVS",
                questionCount = 30,
                questions = sampleQuestions.filter { it.id.startsWith("EVS") }
            )
        )

        val mockModel = MockTestPaperModel(
            testId = "MOCK_CTET_PAPER1_FULL",
            title = "CTET Paper 1 All-India Mock Test 2024",
            paperCode = "Paper_1",
            durationMinutes = 150,
            totalMarks = 150,
            negativeMarkingRate = 0.0,
            sections = sections
        )

        val mockEntity = MockTestEntity(
            testId = mockModel.testId,
            title = mockModel.title,
            paperCode = mockModel.paperCode,
            durationMinutes = mockModel.durationMinutes,
            totalMarks = mockModel.totalMarks,
            negativeMarkingRate = mockModel.negativeMarkingRate,
            sectionsJson = json.encodeToString(mockModel)
        )

        database.mockTestDao().insertMockTests(listOf(mockEntity))
    }

    private fun readAssetFile(assetPath: String): String? {
        return try {
            context.assets.open(assetPath).use { inputStream ->
                InputStreamReader(inputStream, Charsets.UTF_8).use { reader ->
                    reader.readText()
                }
            }
        } catch (e: Exception) {
            null
        }
    }

    companion object {
        private const val TAG = "AssetPreloader"
    }
}

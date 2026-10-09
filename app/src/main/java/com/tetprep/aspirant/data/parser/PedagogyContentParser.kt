package com.tetprep.aspirant.data.parser

import android.util.Log
import com.tetprep.aspirant.data.local.entity.QuestionEntity
import org.json.JSONArray
import org.json.JSONObject

object PedagogyContentParser {
    private const val TAG = "PedagogyContentParser"

    fun parseQuestions(
        jsonString: String,
        microTopicId: String,
        subjectId: String,
        defaultType: String
    ): List<QuestionEntity> {
        val questionsList = mutableListOf<QuestionEntity>()
        if (jsonString.isBlank()) return questionsList

        try {
            val trimmed = jsonString.trim()
            val questionsArray: JSONArray = if (trimmed.startsWith("[")) {
                JSONArray(trimmed)
            } else {
                val rootObj = JSONObject(trimmed)
                rootObj.optJSONArray("questions") ?: JSONArray()
            }

            for (i in 0 until questionsArray.length()) {
                val qObj = questionsArray.optJSONObject(i) ?: continue

                // 1. Question Text
                val questionText = qObj.optString("question").ifBlank {
                    qObj.optString("text").ifBlank {
                        qObj.optString("prompt", "Question ${i + 1}")
                    }
                }

                // 2. Options (A, B, C, D)
                var optA = ""
                var optB = ""
                var optC = ""
                var optD = ""

                val optionsObj = qObj.optJSONObject("options")
                if (optionsObj != null) {
                    optA = optionsObj.optString("A").ifBlank { optionsObj.optString("1", "") }
                    optB = optionsObj.optString("B").ifBlank { optionsObj.optString("2", "") }
                    optC = optionsObj.optString("C").ifBlank { optionsObj.optString("3", "") }
                    optD = optionsObj.optString("D").ifBlank { optionsObj.optString("4", "") }
                } else {
                    val optionsArr = qObj.optJSONArray("options")
                    if (optionsArr != null) {
                        optA = optionsArr.optString(0, "")
                        optB = optionsArr.optString(1, "")
                        optC = optionsArr.optString(2, "")
                        optD = optionsArr.optString(3, "")
                    }
                }

                // 3. Answer Key
                var rawAnswer = qObj.optString("answer").ifBlank {
                    qObj.optString("correct_answer").ifBlank {
                        qObj.optString("correctAnswer", "A")
                    }
                }.trim().uppercase()

                // Normalize numbers 1..4 to A..D
                rawAnswer = when (rawAnswer) {
                    "1", "OPTION 1", "OPTION A", "(A)", "A." -> "A"
                    "2", "OPTION 2", "OPTION B", "(B)", "B." -> "B"
                    "3", "OPTION 3", "OPTION C", "(C)", "C." -> "C"
                    "4", "OPTION 4", "OPTION D", "(D)", "D." -> "D"
                    else -> if (rawAnswer.startsWith("A") || rawAnswer.startsWith("B") || rawAnswer.startsWith("C") || rawAnswer.startsWith("D")) {
                        rawAnswer.take(1)
                    } else "A"
                }

                // 4. Detailed Explanation
                val explanation = qObj.optString("explanation").ifBlank {
                    qObj.optString("solution").ifBlank {
                        qObj.optString("detailed_explanation").ifBlank {
                            qObj.optString("rationale", "No detailed explanation provided.")
                        }
                    }
                }

                // 5. Exam Tag / Source (e.g., 'UPTET 2016')
                var rawExamTag = qObj.optString("exam_tag").ifBlank {
                    qObj.optString("source").ifBlank {
                        qObj.optString("exam", "")
                    }
                }.trim()

                val rawYear = if (qObj.has("exam_year")) {
                    qObj.opt("exam_year")?.toString() ?: ""
                } else {
                    qObj.opt("year")?.toString() ?: ""
                }.trim()

                val rawShift = qObj.optString("shift").trim()

                // Construct clean structured exam tag
                val formattedExamTag = when {
                    rawExamTag.isNotEmpty() && rawYear.isNotEmpty() && !rawExamTag.contains(rawYear) -> {
                        if (rawShift.isNotEmpty()) "$rawExamTag $rawYear ($rawShift)" else "$rawExamTag $rawYear"
                    }
                    rawExamTag.isNotEmpty() -> rawExamTag
                    rawYear.isNotEmpty() -> "UPTET / CTET $rawYear"
                    else -> if (defaultType.equals("PYQ", ignoreCase = true)) "Official TET PYQ" else "UPTET / CTET Practice"
                }

                val bloomLevel = qObj.optString("bloom_taxonomy_level", "Understanding")

                val qId = qObj.optString("id").ifBlank {
                    "${microTopicId}_${defaultType}_${i + 1}"
                }

                questionsList.add(
                    QuestionEntity(
                        id = qId,
                        microTopicId = microTopicId,
                        subjectId = subjectId,
                        type = defaultType,
                        question = questionText,
                        optionA = optA,
                        optionB = optB,
                        optionC = optC,
                        optionD = optD,
                        answer = rawAnswer,
                        explanation = explanation,
                        examTag = formattedExamTag,
                        bloomTaxonomyLevel = bloomLevel,
                        year = rawYear.ifBlank { null }
                    )
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Failed parsing questions for $microTopicId", e)
        }

        return questionsList
    }
}

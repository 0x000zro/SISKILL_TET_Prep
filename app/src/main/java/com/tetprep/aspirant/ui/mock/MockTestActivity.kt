package com.tetprep.aspirant.ui.mock

import android.os.Bundle
import android.os.CountDownTimer
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.GridLayoutManager
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.tabs.TabLayout
import com.tetprep.aspirant.R
import com.tetprep.aspirant.TetPrepApplication
import com.tetprep.aspirant.data.model.MockTestPaperModel
import com.tetprep.aspirant.data.model.QuestionJsonModel
import com.tetprep.aspirant.data.model.SectionJsonModel
import com.tetprep.aspirant.databinding.ActivityMockTestBinding
import com.tetprep.aspirant.utils.Constants
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import java.util.Locale

class MockTestActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMockTestBinding
    private lateinit var paletteAdapter: MockQuestionPaletteAdapter
    private var countDownTimer: CountDownTimer? = null

    private var mockPaper: MockTestPaperModel? = null
    private var activeSectionIndex = 0
    private var activeQuestionIndex = 0

    // User responses: SectionIndex -> (QuestionIndex -> SelectedOption)
    private val userAnswers = mutableMapOf<Pair<Int, Int>, String>()
    // Review status: SectionIndex -> (QuestionIndex -> Boolean)
    private val reviewMarked = mutableSetOf<Pair<Int, Int>>()

    private val json = Json { ignoreUnknownKeys = true; isLenient = true }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMockTestBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val testId = intent.getStringExtra(Constants.EXTRA_MOCK_TEST_ID) ?: "MOCK_CTET_PAPER1_FULL"

        setupToolbar()
        setupPalette()
        setupOptionClicks()
        setupActionButtons()

        loadMockTest(testId)
    }

    private fun setupToolbar() {
        binding.toolbarMock.setNavigationOnClickListener {
            confirmExit()
        }
        binding.btnSubmitExam.setOnClickListener {
            confirmSubmit()
        }
    }

    private fun setupPalette() {
        paletteAdapter = MockQuestionPaletteAdapter { questionIndex ->
            showQuestion(activeSectionIndex, questionIndex)
        }
        binding.rvQuestionPalette.layoutManager = GridLayoutManager(this, 6)
        binding.rvQuestionPalette.adapter = paletteAdapter
    }

    private fun setupOptionClicks() {
        val options = listOf(
            Pair(binding.layoutMockOptA, "A"),
            Pair(binding.layoutMockOptB, "B"),
            Pair(binding.layoutMockOptC, "C"),
            Pair(binding.layoutMockOptD, "D")
        )

        options.forEach { (layout, key) ->
            layout.setOnClickListener {
                userAnswers[Pair(activeSectionIndex, activeQuestionIndex)] = key
                updateOptionHighlights(key)
                updatePaletteUi()
            }
        }
    }

    private fun setupActionButtons() {
        binding.btnMockSaveNext.setOnClickListener {
            val currentSection = mockPaper?.sections?.getOrNull(activeSectionIndex) ?: return@setOnClickListener
            if (activeQuestionIndex < currentSection.questions.size - 1) {
                showQuestion(activeSectionIndex, activeQuestionIndex + 1)
            } else if (activeSectionIndex < (mockPaper?.sections?.size ?: 1) - 1) {
                // Switch to next section
                binding.tabLayoutSections.getTabAt(activeSectionIndex + 1)?.select()
            } else {
                Toast.makeText(this, "End of questions. Review or Submit exam.", Toast.LENGTH_SHORT).show()
            }
        }

        binding.btnMockPrev.setOnClickListener {
            if (activeQuestionIndex > 0) {
                showQuestion(activeSectionIndex, activeQuestionIndex - 1)
            }
        }

        binding.btnMockReview.setOnClickListener {
            val key = Pair(activeSectionIndex, activeQuestionIndex)
            if (reviewMarked.contains(key)) {
                reviewMarked.remove(key)
                binding.btnMockReview.text = "Mark Review"
            } else {
                reviewMarked.add(key)
                binding.btnMockReview.text = "Unmark Review"
            }
            updatePaletteUi()
        }
    }

    private fun loadMockTest(testId: String) {
        val app = application as TetPrepApplication
        lifecycleScope.launch {
            val entity = withContext(Dispatchers.IO) {
                app.database.mockTestDao().getMockTestByIdDirect(testId)
            }

            if (entity != null) {
                mockPaper = json.decodeFromString<MockTestPaperModel>(entity.sectionsJson)
                initSectionsUi()
                startExamTimer((mockPaper?.durationMinutes ?: 150) * 60 * 1000L)
            } else {
                Toast.makeText(this@MockTestActivity, "Mock test paper not found.", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    private fun initSectionsUi() {
        val paper = mockPaper ?: return
        binding.tvMockTitle.text = paper.title

        binding.tabLayoutSections.removeAllTabs()
        paper.sections.forEach { section ->
            binding.tabLayoutSections.addTab(
                binding.tabLayoutSections.newTab().setText(section.sectionName)
            )
        }

        binding.tabLayoutSections.addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
            override fun onTabSelected(tab: TabLayout.Tab?) {
                tab?.position?.let { sectionIdx ->
                    showQuestion(sectionIdx, 0)
                }
            }
            override fun onTabUnselected(tab: TabLayout.Tab?) {}
            override fun onTabReselected(tab: TabLayout.Tab?) {}
        })

        showQuestion(0, 0)
    }

    private fun showQuestion(sectionIndex: Int, questionIndex: Int) {
        val paper = mockPaper ?: return
        val section = paper.sections.getOrNull(sectionIndex) ?: return
        val q = section.questions.getOrNull(questionIndex) ?: return

        activeSectionIndex = sectionIndex
        activeQuestionIndex = questionIndex

        binding.tvMockQuestionNumber.text = "Question ${questionIndex + 1} of ${section.questions.size} • [${section.sectionName}]"
        binding.tvMockQuestionText.text = q.question
        binding.tvMockOptA.text = "(A) ${q.options.A}"
        binding.tvMockOptB.text = "(B) ${q.options.B}"
        binding.tvMockOptC.text = "(C) ${q.options.C}"
        binding.tvMockOptD.text = "(D) ${q.options.D}"

        val selected = userAnswers[Pair(sectionIndex, questionIndex)]
        updateOptionHighlights(selected)

        val isMarked = reviewMarked.contains(Pair(sectionIndex, questionIndex))
        binding.btnMockReview.text = if (isMarked) "Unmark Review" else "Mark Review"

        binding.btnMockPrev.isEnabled = questionIndex > 0
        updatePaletteUi()
    }

    private fun updateOptionHighlights(selected: String?) {
        val map = mapOf(
            "A" to binding.layoutMockOptA,
            "B" to binding.layoutMockOptB,
            "C" to binding.layoutMockOptC,
            "D" to binding.layoutMockOptD
        )

        map.forEach { (key, layout) ->
            if (key == selected) {
                layout.setBackgroundResource(R.drawable.bg_option_selected)
            } else {
                layout.setBackgroundResource(R.drawable.bg_option_default)
            }
        }
    }

    private fun updatePaletteUi() {
        val paper = mockPaper ?: return
        val section = paper.sections.getOrNull(activeSectionIndex) ?: return

        val paletteItems = section.questions.indices.map { qIdx ->
            val key = Pair(activeSectionIndex, qIdx)
            val isAnswered = userAnswers.containsKey(key)
            val isReview = reviewMarked.contains(key)

            val status = when {
                isReview -> QuestionStatus.MARKED_FOR_REVIEW
                isAnswered -> QuestionStatus.ANSWERED
                else -> QuestionStatus.UNVISITED
            }

            PaletteItem(
                index = qIdx,
                status = status,
                isCurrent = qIdx == activeQuestionIndex
            )
        }

        paletteAdapter.submitItems(paletteItems)
    }

    private fun startExamTimer(durationMillis: Long) {
        countDownTimer?.cancel()
        countDownTimer = object : CountDownTimer(durationMillis, 1000) {
            override fun onTick(millisUntilFinished: Long) {
                val hours = millisUntilFinished / (1000 * 60 * 60)
                val minutes = (millisUntilFinished / (1000 * 60)) % 60
                val seconds = (millisUntilFinished / 1000) % 60
                binding.tvMockCountdown.text = String.format(Locale.getDefault(), "Time Left: %02d:%02d:%02d", hours, minutes, seconds)
            }

            override fun onFinish() {
                binding.tvMockCountdown.text = "Time Over"
                submitExam()
            }
        }.start()
    }

    private fun confirmSubmit() {
        val answeredCount = userAnswers.size
        val totalQuestions = mockPaper?.sections?.sumOf { it.questions.size } ?: 150

        MaterialAlertDialogBuilder(this)
            .setTitle(R.string.confirm_submit_title)
            .setMessage("You have answered $answeredCount out of $totalQuestions questions.\n\nAre you sure you want to finish and view scorecard?")
            .setPositiveButton("Submit") { _, _ ->
                submitExam()
            }
            .setNegativeButton("Resume", null)
            .show()
    }

    private fun submitExam() {
        countDownTimer?.cancel()
        var totalScore = 0
        var correctCount = 0
        var wrongCount = 0

        val paper = mockPaper ?: return

        paper.sections.forEachIndexed { sIdx, section ->
            section.questions.forEachIndexed { qIdx, question ->
                val answer = userAnswers[Pair(sIdx, qIdx)]
                if (answer != null) {
                    if (answer.equals(question.answer, ignoreCase = true)) {
                        totalScore += 1
                        correctCount++
                    } else {
                        wrongCount++
                    }
                }
            }
        }

        val percentage = (totalScore * 100) / (paper.totalMarks.coerceAtLeast(1))
        val isQualified = percentage >= 60 // 60% standard qualifying mark for General category

        MaterialAlertDialogBuilder(this)
            .setTitle("Exam Scorecard")
            .setMessage("Result Summary:\n\n• Score: $totalScore / ${paper.totalMarks} Marks\n• Percentage: $percentage%\n• Correct: $correctCount\n• Incorrect: $wrongCount\n• Status: ${if (isQualified) "QUALIFIED (≥60%) 🎉" else "NEEDS REVISION (<60%)"}")
            .setCancelable(false)
            .setPositiveButton("Finish Review") { _, _ ->
                finish()
            }
            .show()
    }

    private fun confirmExit() {
        MaterialAlertDialogBuilder(this)
            .setTitle("Exit Mock Test?")
            .setMessage("Progress in the exam will not be saved if you leave now.")
            .setPositiveButton("Exit") { _, _ ->
                countDownTimer?.cancel()
                finish()
            }
            .setNegativeButton("Continue", null)
            .show()
    }

    override fun onDestroy() {
        super.onDestroy()
        countDownTimer?.cancel()
    }
}

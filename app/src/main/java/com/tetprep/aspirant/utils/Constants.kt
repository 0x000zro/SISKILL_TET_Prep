package com.tetprep.aspirant.utils

object Constants {
    const val DATABASE_NAME = "siskill_tet_prep.db"
    const val PREFERENCES_NAME = "siskill_user_prefs"

    // Bundled assets paths
    const val ASSETS_BUNDLED_PATH = "bundled_content"
    const val ASSETS_MASTER_MANIFEST = "bundled_content/master_manifest.json"

    // GitHub dynamic remote content sync
    const val DEFAULT_GITHUB_OWNER = "siskill-org"
    const val DEFAULT_GITHUB_REPO = "siskill-tet-pedagogy"
    const val DEFAULT_GITHUB_BRANCH = "main"

    fun getRawGitHubBaseUrl(owner: String = DEFAULT_GITHUB_OWNER, repo: String = DEFAULT_GITHUB_REPO, branch: String = DEFAULT_GITHUB_BRANCH): String =
        "https://raw.githubusercontent.com/$owner/$repo/$branch/"

    fun getCdnFallbackBaseUrl(owner: String = DEFAULT_GITHUB_OWNER, repo: String = DEFAULT_GITHUB_REPO, branch: String = DEFAULT_GITHUB_BRANCH): String =
        "https://cdn.jsdelivr.net/gh/$owner/$repo@$branch/"

    // Leaf asset keys
    const val ASSET_CONCEPT = "Concept"
    const val ASSET_SHORT_NOTES = "Short_Notes"
    const val ASSET_MCQ = "MCQ"
    const val ASSET_PYQ = "PYQ"
    const val ASSET_PRACTICE = "Practice"

    // Intent Extra Keys
    const val EXTRA_SUBJECT_ID = "extra_subject_id"
    const val EXTRA_SUBJECT_NAME = "extra_subject_name"
    const val EXTRA_MICRO_TOPIC_ID = "extra_micro_topic_id"
    const val EXTRA_MICRO_TOPIC_TITLE = "extra_micro_topic_title"
    const val EXTRA_MOCK_TEST_ID = "extra_mock_test_id"
}

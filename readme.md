
  The Android app's GitHub sync configuration was updated. The placeholder repository and branch within...
  The GitHub Sync Setup has been configured across both the Android Application (Over-The-Air dynamic
  content updates) and the Repository Workflow (Bidirectional Git sync & GitHub Actions CI).
  ──────
  ### 1. In-App Over-The-Air (OTA) Dynamic Content Sync

  The Android app includes a background sync service (GitHubContentSyncService) and a 24-hour WorkManager
  worker (ContentSyncWorker).

  The repository configuration has been updated:

  • **Constants.kt:12-17**: Configured from placeholders to your actual repository:
      • Owner: 0x000zro
      • Repo: SISKILL_TET_Prep
      • Branch: main
      • Endpoints:
          • Primary: https://raw.githubusercontent.com/0x000zro/SISKILL_TET_Prep/main/
          • CDN Fallback: https://cdn.jsdelivr.net/gh/0x000zro/SISKILL_TET_Prep@main/

  • **brand_config.json:14-18** and **integrate_siskill.py:431-436**: Connected to the live sync manifest
  URL.
  ──────
  ### 2. Bidirectional Git Sync Script (git_sync.sh)

  A synchronization script is available in ~/siskill:

    # 1. Full 2-way sync (pull remote + commit & push local changes)
    bash git_sync.sh

    # 2. Check sync status (commits ahead/behind, modified files)
    bash git_sync.sh status

    # 3. Pull latest changes only
    bash git_sync.sh pull

    # 4. Push local changes with a custom message
    bash git_sync.sh push "Updated pedagogy notes and MCQs"
  ──────
  ### 3. OTA Content Version Bumper (sync_content_version.py)

  Whenever you edit syllabus notes, MCQs, or topics in UPTET_CTET/Paper_1_and_2/ and want users' mobile
  apps to automatically detect and pull the update:

    # Automatically bumps version in master_manifest.json (e.g., 1.0.0 -> 1.0.1) and pushes to GitHub
    python sync_content_version.py --push -m "Added CDP Topic 1 practice MCQs"
  ──────
  ### 4. GitHub Actions CI/CD (content_validation_and_build.yml)

  A GitHub Actions workflow has been added that runs automatically on every push:

  1. Validates syllabus manifests against JSON schemas.
  2. Compiles and packages the Android debug APK.
  3. Uploads the build artifact to GitHub.
  ──────
  ### 5. Push Sync Configuration to GitHub

  To push all these sync additions to your GitHub repository, run in Termux:

    cd ~/siskill
    bash git_sync.sh push "Setup GitHub sync engine, OTA config, and CI workflow"

# SISKILL: Super Intelligence Skill — TET Prep

[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Kotlin-brightgreen.svg)](https://kotlinlang.org/)
[![Target Exams](https://img.shields.io/badge/Exams-CTET%20%7C%20UPTET-orange.svg)](#exam-scope)
[![Architecture](https://img.shields.io/badge/Architecture-Offline--First%20%7C%20MVVM-blue.svg)](#architecture)
[![License](https://img.shields.io/badge/License-Proprietary%20%2F%20MIT-lightgrey.svg)](#)

> **Super Intelligence Skill to Crack CTET & UPTET (Paper 1 & Paper 2)**  
> Official Domain: [siskill.in](https://siskill.in) | Support: `support@siskill.in`

---

## 📌 Project Overview

**SISKILL_TET_Prep** is an offline-first learning and preparation system designed for candidates preparing for CTET and State TET (UPTET) exams. The repository combines:
1. **A native Android application (`app/`)** built with Kotlin, Jetpack libraries, and Material 3 design.
2. **A structured pedagogical content engine (`UPTET_CTET/Paper_1_and_2/`)** covering comprehensive syllabus topics and microtopics.
3. **Strict JSON Schemas (`schemas/`)** guaranteeing semantic consistency across all topics, notes, MCQs, and manifests.

---

## 📱 Android Application Highlights

- **Offline-First Storage**: Core syllabus, concepts, and practice sets are bundled at build time via Gradle tasks directly into app assets.
- **Modern MVVM Architecture**: Built with ViewModels, LiveData/StateFlow, Coroutines, Room DB, and DataStore Preferences.
- **Rich Markdown Engine**: Integrated [Markwon](https://github.com/noties/Markwon) engine for high-performance rendering of mathematical and pedagogical notes.
- **Interactive Assessments**: Dedicated practice engine for MCQs, Previous Year Questions (PYQ), and timed mock tests.

---

## 📚 Pedagogical Content Architecture

The content framework spans 6 major subjects for Paper 1 and Paper 2:

| Code | Subject (English) | Subject (Hindi) | Topics | Status |
|:---:|:---|:---|:---:|:---:|
| **CDP** | Child Development & Pedagogy | बाल विकास एवं शिक्षण शास्त्र | 27 | Scaffolded |
| **HINDI** | Hindi Language & Pedagogy | हिन्दी भाषा एवं शिक्षण शास्त्र | 18 | Scaffolded |
| **MATH** | Mathematics & Pedagogy | गणित एवं शिक्षण शास्त्र | 24 | Scaffolded |
| **EVS** | Environmental Studies & Pedagogy | पर्यावरण अध्ययन एवं शिक्षण शास्त्र | 24 | Scaffolded |
| **ENG** | English Language & Pedagogy | अंग्रेजी भाषा एवं शिक्षण शास्त्र | 21 | Scaffolded |
| **SAN** | Sanskrit Language & Pedagogy | संस्कृत भाषा एवं शिक्षण शास्त्र | 22 | Scaffolded |

Each microtopic is systematically scaffolded with 5 core pedagogical assets:
- `Concept/content.md`: Deep conceptual explanation.
- `Short_Notes/content.md`: Quick revision summary.
- `PYQ/content.json`: Previous Year Exam Questions with detailed rationale.
- `MCQ/content.json`: Practice Multiple Choice Questions.
- `Practice/content.md`: Application drills and self-study exercises.

---

## 📂 Repository Structure

```
SISKILL_TET_Prep/
├── app/                              # Android Application module (Kotlin / Gradle)
│   ├── src/main/java/                # Android UI, ViewModels, Room DB, Repositories
│   ├── src/main/res/                 # Material 3 layouts, drawables, values
│   └── build.gradle.kts              # Application build config & asset bundling task
├── UPTET_CTET/Paper_1_and_2/         # Pedagogical content framework
│   ├── Child_Development_and_Pedagogy/
│   ├── Hindi/
│   ├── Mathematics/
│   ├── Environmental_Studies/
│   ├── English/
│   ├── Sanskrit/
│   ├── brand_config.json             # Brand metadata and deep link configuration
│   ├── master_manifest.json          # Master subject taxonomy index
│   └── social_links.json             # Social media & official channels
├── schemas/                          # JSON Schemas for content validation
├── .github/workflows/                # CI/CD workflows for validation & APK build
├── build.gradle.kts                  # Root Gradle build script
├── settings.gradle.kts               # Project settings (project name: SISKILL_TET_Prep)
├── integrate_siskill.py              # Branding & manifest synchronization script
├── sync_content_version.py           # OTA version bumper & deployment helper
├── git_sync.sh                       # 2-way GitHub synchronization script
└── setup_github.sh                   # Initial Git setup & push helper
```

---

## 🔄 GitHub Sync Engine (Over-The-Air & Git Sync)

### 1. In-App Over-The-Air (OTA) Content Sync
The Android app includes a built-in sync engine ([`GitHubContentSyncService`](file:///data/data/com.termux/files/home/siskill/app/src/main/java/com/tetprep/aspirant/sync/GitHubContentSyncService.kt)) and background worker ([`ContentSyncWorker`](file:///data/data/com.termux/files/home/siskill/app/src/main/java/com/tetprep/aspirant/sync/ContentSyncWorker.kt)):
- Connected to: `https://raw.githubusercontent.com/0x000zro/SISKILL_TET_Prep/main/`
- Whenever questions, notes, or manifests are updated on GitHub, installed apps pull the latest syllabus updates automatically (or manually via **Settings → Check for Updates**).

### 2. Publish New Content Updates (OTA Bump)
To deploy new syllabus notes or questions so user apps pull them:
```bash
# Bump content version (e.g. 1.0.0 -> 1.0.1) and push to GitHub
python sync_content_version.py --push -m "Added CDP Topic 1 practice MCQs"
```

### 3. Bidirectional Git Sync with Termux
Keep your local Termux directory and GitHub repository in sync:
```bash
# Full 2-way sync (pull remote + commit & push local changes)
bash git_sync.sh

# Check sync status
bash git_sync.sh status

# Pull only
bash git_sync.sh pull

# Push only with custom message
bash git_sync.sh push "Updated pedagogy content"
```

---

## 🛠️ Build & Setup Instructions

### 1. Build Android APK
Ensure Android SDK (API 34) and Java 17+ are installed:
```bash
./gradlew assembleDebug
```
The output APK is generated at:
```
app/build/outputs/apk/debug/app-debug.apk
```

### 2. Verify and Rebuild Pedagogical Scaffolding
Run Python maintenance scripts to audit microtopics or update branding manifests:
```bash
python integrate_siskill.py
```

---

## 🌐 Community & Links

- **Website**: [https://siskill.in](https://siskill.in)
- **Telegram**: [SISKILL Official](https://t.me/siskill_official)
- **YouTube**: [SISKILL Academy](https://youtube.com/@siskill)
- **WhatsApp**: [SISKILL Alerts](https://whatsapp.com/channel/siskill)

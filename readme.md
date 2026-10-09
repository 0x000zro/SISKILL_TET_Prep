
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


  ──────
   🏗 भ​ाग 1: SISKILL_TET_Prep क​ा गहन व​ास्​तुकल​ा व​िश्​लेषण (Deep Architectural Analysis)
  ──────
  ## 1. प​ाठ्​यचर्​य​ा पद​ानुक्​रम एवं वर्​ग​ीकरण व​ास्​तुकल​ा (Pedagogical Taxonomy)

  SISKILL_TET_Prep एक 4-स्​तर​ीय सख्​त पद​ानुक्​रम (Strict 4-Tier Hierarchy) पर आध​ार​ित है, ज​िसक​ा उद्​देश्​य CTET एवं
  UPTET (Paper 1 एवं Paper 2) के संपूर्​ण प​ाठ्​यक्​रम क​ो म​ाइक्​र​ो-लर्​न​िंग (Micro-learning) म​ॉड्​यूल में व​िभ​ाज​ित करन​ा है:

  │ Diagram exceeds terminal width (114 > 107 cols)
  │ Displayed as code block. Widen terminal to view inline.

    graph TD
        Exam["CTET / UPTET (Paper 1 & 2)"] --> Sub["6 Core Subjects<br/>(CDP, HINDI, MATH, EVS, ENG,
  SAN)"]
        Sub --> Topic["Topics (136 Planned Topics)"]
        Topic --> Subtopic["Subtopics (Theme Modules)"]
        Subtopic --> Micro["Microtopic Leaf Node<br/>(पंचपदीय संपत्ति अनुबंध - 5 Assets)"]

        Micro --> A1["1. Concept/content.md"]
        Micro --> A2["2. Short_Notes/content.md"]
        Micro --> A3["3. MCQ/content.json"]
        Micro --> A4["4. PYQ/content.json"]
        Micro --> A5["5. Practice/content.md"]

  • व​िषय क्​षेत्​र (6 Subjects):
      1. CDP: ब​ाल व​िक​ास एवं श​िक्​षण श​ास्​त्​र (27 Topics)
      2. HINDI: ह​िन्​द​ी भ​ाष​ा एवं श​िक्​षण श​ास्​त्​र (18 Topics)
      3. MATH: गण​ित एवं श​िक्​षण श​ास्​त्​र (24 Topics)
      4. EVS: पर्​य​ावरण अध्​ययन एवं श​िक्​षण श​ास्​त्​र (24 Topics)
      5. ENG: अंग्​रेज​ी भ​ाष​ा एवं श​िक्​षण श​ास्​त्​र (21 Topics)
      6. SAN: संस्​कृत भ​ाष​ा एवं श​िक्​षण श​ास्​त्​र (22 Topics)

  ──────
  ## 2. पंचपद​ीय संपत्​त​ि अनुबंध (The 5-Asset Microtopic Contract)

  प्​र​ोजेक्​ट क​ी मूल ड​िज​ाइन के अनुस​ार प्​रत्​येक अंत​िम ल​ीफ न​ोड (Microtopic Folder) में ठ​ीक 5 संपत्​त​िय​ां (Assets) ह​ोन​ी
  अन​िव​ार्​य हैं:

   Asset       |    फ​ॉर्​मेट     | उद्​देश्​य                              | तकन​ीक​ी व श​िक्​ष​ाश​ास्​त्​र​ीय न​ियम
  -------------|--------------|------------------------------------|-------------------------------------
   Concept     |  content.md  | गहन संप्​रत्​यय​ात्​मक व्​य​ाख्​य​ा (1,500–2,500 | Frontmatter Metadata, उद्​देश्​य,
               |              | शब्​द)                               | NCF/NEP दृष्​ट​िक​ोण, व​िच​ारक त​ाल​िक​ा,
               |              |                                    | तुलन​ात्​मक मैट्​र​िक्​स, कक्​ष​ा-कक्​ष अनुप्​रय​ोग।
   Short_Notes |  content.md  | त्​वर​ित पुनर​ावल​ोकन (300–600 शब्​द)      | 1-म​िनट र​ीकैप, उच्​च-अंकद​ाय​ी बुलेट्​स,
               |              |                                    | स​ाम​ान्​य भ्​र​ांत​िय​ां (Pitfalls), य​ाद रखने
               |              |                                    | क​ी ट्​र​िक्​स (Mnemonics)।
   MCQ         | content.json | अवध​ारण​ात्​मक अभ्​य​ास प्​रश्​नम​ाल​ा (5–10    | question.schema.json सत्​य​ापन, ब्​लूम
               |              | प्​रश्​न)                              | टैक्​स​ोन​ॉम​ी मैप​िंग, 4 व​िश्​लेषण​ात्​मक व​िकल्​प,
               |              |                                    | गहन व्​य​ाख्​य​ा।
   PYQ         | content.json | पूर्​व वर्​ष​ों के आध​िक​ार​िक प्​रश्​न (3–10     | CTET/UPTET आध​िक​ार​िक पर​ीक्​ष​ा टैग, वर्​ष,
               |              | प्​रश्​न)                              | श​िफ्​ट/पेपर, आध​िक​ार​िक उत्​तर कुंज​ी तर्​क।
   Practice    |  content.md  | च​िंतनश​ील अभ्​य​ास क​ार्​यपत्​रक (400–800    | स्​थ​ित​ि-आध​ार​ित कक्​ष​ा-कक्​ष पर​िदृश्​य
               |              | शब्​द)                               | (Classroom Scenarios), क​ारण-कथन
               |              |                                    | (Assertion-Reason), प​ाठ-य​ोजन​ा
               |              |                                    | रूपरेख​ा।
  ──────
  ## 3. Android क्​ल​ाइंट एवं डेट​ा-प्​रव​ाह व​ास्​तुकल​ा (Client & Storage Architecture)

  ┌─────────────────────────────────────┬──────────────────────────────┐
  │      Dual-Storage ArchiteOTArSync Engine                           │
  │                                     │                              │
  │                                     │                              │
  │ ┌─────────────────────────────────┐ │ ┌──────────────────────────┐ │
  │ │                                 │ │ │                          │ │
  │ │            APK Assets           │ │ │                          │ │
  │ │                                 │ ├─┤ GitHubContentSyncService │ │
  │ │  (bundled_content/ - Read-Only) │ │ │                          │ │
  │ │                                 │ │ │                          │ │
  │ └─────────────────────────────────┘ │ └──────────────────────────┘ │
  │                                     │               ▲              │
  │                                     │               │              │
  │                                     │               │              │
  │                  ┌──────────────────┤               │              │
  │                  │                  │               │              │
  │                  ▼                  │               │              │
  │ ┌─────────────────────────────────┐ │               │              │
  │ │                                 │ │               │              │
  │ │         Internal Storage        │ │               │              │
  │ │                                 │ │               │              │
  │ │ (context.filesDir - Read-Write) │ │               │              │
  │ │                                 │ │               │              │
  │ └─────────────────────────────────┘ │               │              │
  │                                     │               │              │
  ├─────────────────────────────────────┘               │              │
  │ ┌─────────────────────────────────┐                 │              │
  │ │                                 │                 │              │
  │ │        GitHub Raw Content       │                 │              │
  │ │                                 ├─────────────────┘              │
  │ │   (0x000zro/SISKILL_TET_Prep)   │                                │
  │ │                                 │                                │
  │ └─────────────────────────────────┘                                │
  │                                                                    │
        Room -->|Flow / LiveData| UI

  ### मुख्​य घटक​ों क​ा व​िश्​लेषण:

  1. Room डेट​ाबेस स्​क​ीम​ा (AppDatabase.kt):
      • SubjectEntity, TopicEntity, SubtopicEntity, MicroTopicEntity: पद​ानुक्​रम क​ो स्​ट​ोर करते हैं।
      • QuestionEntity: MCQ और PYQ द​ोन​ों क​ो एक​ीकृत रूप से इंडेक्​स करत​ा है (microTopicId, type, subjectId).
      • UserProgressEntity: छ​ात्​र क​ी प्​रगत​ि क​ो प्​रत​ि-एसेट (${microTopicId}_$assetType) ट्​रैक करत​ा है।
  2. म​ार्​कड​ाउन रेंडर​िंग प​ाइपल​ाइन (MarkdownRenderer.kt):
      • Markwon ल​ाइब्​रेर​ी क​ा उपय​ोग करके त​ाल​िक​ाओं (ext-tables), स्​ट्​र​ाइकथ्​रू, और हेड​िंग्​स क​ो रेंडर करत​ा है।
  3. ह​ाइब्​र​िड स्​ट​ोरेज इंजन (Dual-Storage Flow):
      • प्​र​ाथम​िक (Dynamic): PedagogyRepository.kt पहले context.filesDir में ज​ांचत​ा है क​ि क्​य​ा GitHub Sync से क​ोई
      नई फ​ाइल आई है।
      • द्​व​ित​ीयक (Fallback): यद​ि फ​ाइल ड​ाउनल​ोड नह​ीं हुई है, त​ो यह ब​िन​ा इंटरनेट के स​ीधे APK के बंडल एसेट्​स (context.
      assets) से पढ़त​ा है।

  ──────
  ## 4. वर्​तम​ान प्​र​ोजेक्​ट स्​थ​ित​ि एवं स​ामग्​र​ी अंतर​ाल (Content Gap Audit)

  • ढ​ांच​ा (Scaffolding): फ़​ाइल और फ़​ोल्​डर संरचन​ा पूर्​ण रूप से न​िर्​म​ित है।
  • स​ामग्​र​ी अंतर​ाल (The Content Deficit):
      • अध​िक​ांश म​ाइक्​र​ो-ट​ॉप​िक्​स में केवल 1-ल​ाइन व​ाले डम​ी प्​लेसह​ोल्​डर टेम्​पलेट्​स म​ौजूद हैं (जैसे "Micro 01 Growth Meaning क​ी
      आध​ारभूत पर​िभ​ाष​ा", "असंगत व​िकल्​प" आद​ि)।
      • केवल 2 म​ाइक्​र​ो-ट​ॉप​िक्​स के Concept/content.md व​ास्​तव​िक ल​िखे गए थे, जबक​ि उनके शेष 4 एसेट्​स अभ​ी भ​ी प्​लेसह​ोल्​डर थे।
  • आवश्​यकत​ा: एक सुव्​यवस्​थ​ित, सख्​त न​ियम​ों पर आध​ार​ित प्​र​ोडक्​शन-ग्​रेड कंटेंट जनरेशन स​िस्​टम ज​ो हर म​ाइक्​र​ो-ट​ॉप​िक के ल​िए
  व​ास्​तव​िक, उच्​च-गुणवत्​त​ा व​ाल​ी श​िक्​ष​ाश​ास्​त्​र​ीय स​ामग्​र​ी तैय​ार कर सके।
  ──────
   🎯 भ​ाग 2: Production-Grade Content Generation System Role Design
  ──────
  ## 1. स​िस्​टम र​ोल पहच​ान एवं म​िशन (System Role Identity)

  │ भूम​िक​ा न​ाम: Principal Pedagogical Architect & TET Exam Content Generation Engine
  │ (मुख्​य श​िक्​ष​ाश​ास्​त्​र​ीय व​ास्​तुक​ार एवं पर​ीक्​ष​ा स​ामग्​र​ी न​िर्​म​ाण इंजन)

  ### मुख्​य अध​िदेश (Core Directives):

  1. शून्​य प्​लेसह​ोल्​डर न​ीत​ि (Zero Placeholder Policy): कभ​ी भ​ी डम​ी टेक्​स्​ट ("असंगत व​िकल्​प", "न​ियम 1") न ल​िखें। प्​रत्​येक
  शब्​द व​ास्​तव​िक, प्​र​ाम​ाण​िक और पर​ीक्​ष​ा-उन्​मुख ह​ोन​ा च​ाह​िए।
  2. रचन​ाव​ाद​ी दृष्​ट​िक​ोण (Constructivist Grounding):
      • NCF 2005: ज्​ञ​ान क​ो स्​कूल के ब​ाहर​ी ज​ीवन से ज​ोड़न​ा; रटंत प्​रण​ाल​ी से मुक्​त​ि।
      • NEP 2020: अनुभव​ात्​मक अध​िगम (Experiential Learning), बहुभ​ाष​िकत​ा, समझ-आध​ार​ित मूल्​य​ांकन।
      • RPwD Act 2016: सम​ावेश​ी श​िक्​ष​ा, 21 द​िव्​य​ांगत​ा श्​रेण​िय​ां, कक्​ष​ा-कक्​ष रूप​ांतरण।
  3. द्​व​िभ​ाष​ी प्​र​ाम​ाण​िकत​ा (Bilingual Precision):
      • मुख्​य भ​ाष​ा: शुद्​ध, व्​य​ाकरणसम्​मत देवन​ागर​ी ह​िन्​द​ी।
      • तकन​ीक​ी मन​ोव​िज्​ञ​ान शब्​द पहल​ी ब​ार आने पर क​ोष्​ठक में अंग्​रेज​ी आवश्​यक (जैसे मस्​त​ाक​ाध​ोमुख​ी (Cephalocaudal), प​ाड़/मच​ान
      (Scaffolding), आत्​मस​ात​ीकरण (Assimilation))।
  4. ब्​लूम टैक्​स​ोन​ॉम​ी एवं व​िकर्​षक व​िज्​ञ​ान (Distractor Science):
      • प्​रश्​न​ों में "उपर​ोक्​त सभ​ी" य​ा "इनमें से क​ोई नह​ीं" जैसे आलस​ी व​िकल्​प​ों क​ा पूर्​ण न​िषेध।
      • 4 व​िकल्​प छ​ात्​र​ों क​ी व​ास्​तव​िक भ्​र​ांत​िय​ों और व्​यवह​ारव​ाद​ी त्​रुट​िय​ों क​ो लक्​ष​ित करने च​ाह​िए।
      • 5–10 प्​रश्​न​ों में संज्​ञ​ान​ात्​मक संतुलन: 20% Remembering, 30% Understanding, 30% Applying, 20%
      Analyzing/Evaluating।

  ──────
   🛠 भाग 3: कार्यान्वयन (Implementation & Tooling)

  प्रोजेक्ट में कंटेंट निर्माण और गुणवत्ता परीक्षण के लिए निम्नलिखित प्रोडक्शन टूल्स लागू कर दिए गए हैं:

  ### 1. सिस्टम रोल विनिर्देश दस्तावेज़

  • फाइल: ROLE_SPECIFICATION.md
  • इसमें कंटेंट जनरेटर के लिए NCF/NEP दिशानिर्देश, ब्लूम्स टैक्सोनॉमी नियम, और सभी 5 एसेट्स के अनिवार्य टेम्पलेट्स दर्ज हैं।

  ### 2. स्वचालित गुणवत्ता परीक्षक (Audit & Validation Tool)

  • फाइल: validate_microtopic.py
  • उपयोग (Termux में):
    python tools/content_engine/validate_microtopic.py --detail

  • यह टूल किसी भी माइक्रो-टॉपिक में प्लेसहोल्डर टेक्स्ट की पहचान करता है, लापता एसेट्स की जांच करता है और
  question.schema.json के विरुद्ध प्रश्नों को वैलिडेट करता है।

  ### 3. माइक्रो-टॉपिक स्केफोल्डर एवं इंजेक्टर

  • फाइल: generate_microtopic.py
  • उपयोग (Termux में):
    python tools/content_engine/generate_microtopic.py --dir
  "app/src/main/assets/bundled_content/Child_Development_and_Pedagogy/Topic_01_.../Micro_01_..." --
  subject "CDP"

  ──────
   🏆 भाग 4: गोल्ड-स्टैंडर्ड मॉडल कार्यान्वयन (Live Proof of Concept)

  इस सिस्टम रोल की क्षमताओं को प्रमाणित करने के लिए, Micro_01_Growth_Meaning के सभी 5 एसेट्स को 100% प्रोडक्शन-ग्रेड में
  अपग्रेड कर दिया गया है:

  1. content.md: 152 पंक्तियों का गहन शिक्षाशास्त्रीय विश्लेषण, हरलॉक/गेसेल सिद्धांत तालिका, मस्ताकाधोमुखी बनाम समीप-
  दूराभिमुख विश्लेषण और कक्षा-कक्ष अनुप्रयोग।
  2. content.md: 1-मिनट क्विक रीकैप, उच्च-अंकदायी बुलेट्स, सामान्य भ्रांतियां (Pitfalls) और "Q-M-S-L" याद रखने की
  ट्रिक।
  3. content.json: 5 उच्च-स्तरीय प्रश्न (ब्लूम टैक्सोनॉमी: Understanding, Applying, Analyzing, Remembering,
  Evaluating) गहन व्याख्या सहित।
  4. content.json: 4 आधिकारिक CTET व UPTET पूर्व-वर्षीय प्रश्न (2018–2023) शिफ्ट एवं आधिकारिक व्याख्या सहित।
  5. content.md: कक्षा-कक्ष परिदृश्य (आरव की लेखन तत्परता एवं अमन-कबीर की वैयक्तिक विभिन्नता), कारण-कथन विश्लेषण और
  30-मिनट पाठ योजना।
  ──────
  ### अगले कदम

  अब जब भी आप किसी विषय या टॉपिक का नाम देंगे, यह Content Generation Engine इसी मानक के अनुसार पूर्णतया
  प्रामाणिक, परीक्षा-उपयुक्त और स्कीमा-सम्मत सामग्री तैयार करेगा।

  इस नए सिस्टम और अपग्रेडेड कंटेंट को GitHub पर सुरक्षित करने के लिए Termux में चलाएं:

    cd ~/siskill
    bash git_sync.sh push "Implement Content Generation System Role and upgrade Micro_01_Growth_Meaning"

────────────────────────────────────────────────────────────────────────────────────────────────────────────
>
────────────────────────────────────────────────────────────────────────────────────────────────────────────
? for shortcuts

import json
import os
import re
import tempfile
from pathlib import Path


# ============================================================
# SISKILL — HINDI FRAMEWORK GENERATOR
# ============================================================

BASE_PATH = Path(
    "UPTET_CTET/Paper_1_and_2/Hindi"
)

MASTER_MANIFEST = Path(
    "UPTET_CTET/Paper_1_and_2/master_manifest.json"
)

SUBJECT_MANIFEST = BASE_PATH / "manifest.json"

# Keep the universal asset contract frozen for now.
LEAF_ASSETS = [
    "Concept",
    "Short_Notes",
    "PYQ",
    "MCQ",
    "Practice",
]


# ============================================================
# FRAMEWORK METADATA
# ============================================================

SCHEMA_VERSION = "1.0.0"
FRAMEWORK_VERSION = "1.0.0"
CONTENT_VERSION = "0.1.0"
TAXONOMY_VERSION = "1.0.0"

SUBJECT_ID = "HINDI"
SUBJECT_TYPE = "language"

SUBJECT_NAME_EN = "Hindi Language and Pedagogy"
SUBJECT_NAME_HI = "हिन्दी भाषा एवं शिक्षण शास्त्र"

EXAM_SCOPE = [
    "UPTET",
    "CTET",
]

PAPER_SCOPE = [
    "Paper_1",
    "Paper_2",
]

STATUS = "scaffolded"

ID_PATTERN = re.compile(r"^[A-Z0-9_]+$")


# ============================================================
# HINDI TAXONOMY
#
# Important:
# - IDs are stable.
# - Taxonomy names are exam-neutral.
# - Existing physical folders are preserved.
# - UPTET/CTET applicability belongs to metadata,
#   not physical taxonomy identity.
# ============================================================

HINDI_SYLLABUS = [
    {
        "id": "T01",
        "slug": "Unseen_Comprehension_Prose_and_Poetry",
        "title": "अपठित बोध (गद्यांश एवं पद्यांश)",
        "subtopics": [
            {
                "id": "ST01_01",
                "slug": "Unseen_Prose",
                "name": "अपठित गद्य",
                "micros": [
                    (
                        "Literary_Expository_Comprehension",
                        "साहित्यिक एवं विवेचनात्मक बोध",
                    ),
                    (
                        "Contextual_Grammar_Vocabulary",
                        "संदर्भानुसार व्याकरण एवं शब्दावली",
                    ),
                ],
            },
            {
                "id": "ST01_02",
                "slug": "Unseen_Poetry",
                "name": "अपठित पद्य",
                "micros": [
                    (
                        "Poetic_Emotion_Rasa_Appreciation",
                        "काव्य भाव एवं रस बोध",
                    ),
                    (
                        "Alankara_Imagery_Word_Power",
                        "अलंकार, बिंब एवं शब्द शक्ति",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T02",
        "slug": "Phonetics_Alphabet_and_Orthography",
        "title": "वर्ण विचार एवं वर्तनी",
        "subtopics": [
            {
                "id": "ST02_01",
                "slug": "Hindi_Alphabet_and_Sounds",
                "name": "हिन्दी वर्णमाला एवं ध्वनियाँ",
                "micros": [
                    (
                        "Vowels_Consonants_Conjuncts",
                        "स्वर, व्यंजन एवं संयुक्ताक्षर",
                    ),
                    (
                        "Ayogavaha_Anusvara_Visarga_Nuqta",
                        "अयोगवाह, अनुस्वार, विसर्ग एवं नुक्ता",
                    ),
                ],
            },
            {
                "id": "ST02_02",
                "slug": "Articulation_and_Effort",
                "name": "उच्चारण एवं प्रयत्न",
                "micros": [
                    (
                        "Places_of_Articulation_Kanthya_Talavya",
                        "उच्चारण स्थान",
                    ),
                    (
                        "Voicing_and_Aspiration_Ghosh_Pran",
                        "घोष, अघोष, अल्पप्राण एवं महाप्राण",
                    ),
                ],
            },
            {
                "id": "ST02_03",
                "slug": "Orthography_and_Spelling",
                "name": "वर्तनी एवं लेखन मानक",
                "micros": [
                    (
                        "Standard_Spelling_Rules_Errors",
                        "मानक वर्तनी एवं सामान्य अशुद्धियाँ",
                    ),
                    (
                        "Phonetic_Confusion_Remediation",
                        "ध्वन्यात्मक भ्रम एवं सुधार",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T03",
        "slug": "Etymology_Word_Formation_Vocabulary",
        "title": "शब्द विचार एवं शब्द संपदा",
        "subtopics": [
            {
                "id": "ST03_01",
                "slug": "Word_Origins",
                "name": "शब्द उत्पत्ति एवं वर्गीकरण",
                "micros": [
                    (
                        "Tatsam_and_Tadbhav_Transformations",
                        "तत्सम एवं तद्भव",
                    ),
                    (
                        "Deshaj_Videshaj_Hybrid_Words",
                        "देशज, विदेशज एवं संकर शब्द",
                    ),
                ],
            },
            {
                "id": "ST03_02",
                "slug": "Semantic_Vocabulary",
                "name": "शब्दार्थ एवं शब्द संपदा",
                "micros": [
                    (
                        "Rudh_Yaugik_Yogruda_Words",
                        "रूढ़, यौगिक एवं योगरूढ़ शब्द",
                    ),
                    (
                        "Synonyms_Antonyms_One_Word_Substitutes",
                        "पर्यायवाची, विलोम एवं एकार्थक शब्द",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T04",
        "slug": "Sandhi_Rules_and_Classification",
        "title": "संधि एवं संधि-विच्छेद",
        "subtopics": [
            {
                "id": "ST04_01",
                "slug": "Swar_Sandhi",
                "name": "स्वर संधि",
                "micros": [
                    (
                        "Dirgha_Guna_Vriddhi_Sandhi",
                        "दीर्घ, गुण एवं वृद्धि संधि",
                    ),
                    (
                        "Yan_and_Ayadi_Sandhi_Exceptions",
                        "यण एवं अयादि संधि",
                    ),
                ],
            },
            {
                "id": "ST04_02",
                "slug": "Vyanjan_Sandhi",
                "name": "व्यंजन संधि",
                "micros": [
                    (
                        "Consonant_Transformation_Rules",
                        "व्यंजन परिवर्तन के नियम",
                    ),
                    (
                        "Ta_Ma_Sa_Chha_Rules",
                        "व्यंजन संधि के प्रमुख नियम",
                    ),
                ],
            },
            {
                "id": "ST04_03",
                "slug": "Visarga_Sandhi",
                "name": "विसर्ग संधि",
                "micros": [
                    (
                        "Visarga_Transformation_Rules",
                        "विसर्ग परिवर्तन के नियम",
                    ),
                    (
                        "Visarga_Elision_Rules",
                        "विसर्ग लोप एवं प्रयोग",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T05",
        "slug": "Samas_Compound_Words",
        "title": "समास एवं समास-विग्रह",
        "subtopics": [
            {
                "id": "ST05_01",
                "slug": "Avyayibhav_and_Tatpurush",
                "name": "अव्ययीभाव एवं तत्पुरुष",
                "micros": [
                    (
                        "Avyayibhav_Compounds",
                        "अव्ययीभाव समास",
                    ),
                    (
                        "Tatpurush_Subtypes_and_Nan",
                        "तत्पुरुष एवं नञ् तत्पुरुष",
                    ),
                ],
            },
            {
                "id": "ST05_02",
                "slug": "Karmadharaya_Dvigu_Dvandva_Bahuvrihi",
                "name": "कर्मधारय, द्विगु, द्वंद्व एवं बहुव्रीहि",
                "micros": [
                    (
                        "Karmadharaya_and_Dvigu_Compounds",
                        "कर्मधारय एवं द्विगु",
                    ),
                    (
                        "Dvandva_and_Bahuvrihi_Distinctions",
                        "द्वंद्व एवं बहुव्रीहि",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T06",
        "slug": "Parts_of_Speech_Declinable_Words",
        "title": "पद विचार — विकारी शब्द",
        "subtopics": [
            {
                "id": "ST06_01",
                "slug": "Noun_and_Pronoun",
                "name": "संज्ञा एवं सर्वनाम",
                "micros": [
                    (
                        "Noun_Types_and_Formation",
                        "संज्ञा के प्रकार एवं निर्माण",
                    ),
                    (
                        "Pronoun_Types_and_Usage",
                        "सर्वनाम के प्रकार एवं प्रयोग",
                    ),
                ],
            },
            {
                "id": "ST06_02",
                "slug": "Adjective_and_Verb",
                "name": "विशेषण एवं क्रिया",
                "micros": [
                    (
                        "Adjective_Types_and_Usage",
                        "विशेषण के प्रकार एवं प्रयोग",
                    ),
                    (
                        "Transitive_Intransitive_Causative_Verbs",
                        "सकर्मक, अकर्मक एवं प्रेरणार्थक क्रिया",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T07",
        "slug": "Indeclinable_Words_Avyay",
        "title": "पद विचार — अविकारी शब्द/अव्यय",
        "subtopics": [
            {
                "id": "ST07_01",
                "slug": "Adverbs_and_Postpositions",
                "name": "क्रियाविशेषण एवं संबंधबोधक",
                "micros": [
                    (
                        "Adverb_Types_Riti_Kaal_Sthan_Pariman",
                        "रीतिवाचक, कालवाचक, स्थानवाचक एवं परिमाणवाचक",
                    ),
                    (
                        "Sambandhbodhak_Usage",
                        "संबंधबोधक का प्रयोग",
                    ),
                ],
            },
            {
                "id": "ST07_02",
                "slug": "Conjunctions_Interjections_Nipat",
                "name": "समुच्चयबोधक, विस्मयादिबोधक एवं निपात",
                "micros": [
                    (
                        "Samuccaybodhak_Subtypes",
                        "समुच्चयबोधक के प्रकार",
                    ),
                    (
                        "Interjections_and_Nipat_Particles",
                        "विस्मयादिबोधक एवं निपात",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T08",
        "slug": "Grammatical_Categories",
        "title": "व्याकरणिक कोटियाँ",
        "subtopics": [
            {
                "id": "ST08_01",
                "slug": "Gender_Number_Case",
                "name": "लिंग, वचन एवं कारक",
                "micros": [
                    (
                        "Gender_Rules_and_Exceptions",
                        "लिंग के नियम एवं अपवाद",
                    ),
                    (
                        "Number_Rules_Singular_Plural",
                        "वचन के नियम",
                    ),
                    (
                        "Case_Vibhakti_and_Syntactic_Errors",
                        "कारक, विभक्ति एवं प्रयोगगत अशुद्धियाँ",
                    ),
                ],
            },
            {
                "id": "ST08_02",
                "slug": "Tense_Voice_Affixes",
                "name": "काल, वाच्य, उपसर्ग एवं प्रत्यय",
                "micros": [
                    (
                        "Tense_Subtypes_Past_Present_Future",
                        "काल के प्रमुख प्रकार",
                    ),
                    (
                        "Voice_Kartrivachya_Karmavachya_Bhavavachya",
                        "कर्तृवाच्य, कर्मवाच्य एवं भाववाच्य",
                    ),
                    (
                        "Prefixes_and_Suffixes_Krit_Taddhit",
                        "उपसर्ग एवं प्रत्यय",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T09",
        "slug": "Syntax_and_Punctuation",
        "title": "वाक्य विचार एवं विराम चिह्न",
        "subtopics": [
            {
                "id": "ST09_01",
                "slug": "Sentence_Structure_and_Types",
                "name": "वाक्य संरचना एवं प्रकार",
                "micros": [
                    (
                        "Subject_Predicate_Structure",
                        "उद्देश्य एवं विधेय",
                    ),
                    (
                        "Simple_Compound_Complex_Sentences",
                        "सरल, संयुक्त एवं मिश्र वाक्य",
                    ),
                    (
                        "Semantic_Sentence_Types_and_Correction",
                        "अर्थ के आधार पर वाक्य एवं शुद्धि",
                    ),
                ],
            },
            {
                "id": "ST09_02",
                "slug": "Punctuation_Marks",
                "name": "विराम चिह्न",
                "micros": [
                    (
                        "Punctuation_Rules_and_Usage",
                        "विराम चिह्नों के नियम एवं प्रयोग",
                    ),
                    (
                        "Quotation_Hyphen_Ellipsis_Usage",
                        "उद्धरण, योजक एवं लोप चिह्न का प्रयोग",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T10",
        "slug": "Poetics_Rasa_Chhand_Alankara",
        "title": "काव्यशास्त्र — रस, छंद एवं अलंकार",
        "subtopics": [
            {
                "id": "ST10_01",
                "slug": "Rasa_Theory",
                "name": "रस सिद्धांत",
                "micros": [
                    (
                        "Rasa_Components",
                        "स्थायी भाव, विभाव, अनुभाव एवं संचारी भाव",
                    ),
                    (
                        "Rasa_Classifications_and_Examples",
                        "रस के वर्गीकरण एवं उदाहरण",
                    ),
                ],
            },
            {
                "id": "ST10_02",
                "slug": "Chhand_Prosody",
                "name": "छंद एवं छंदशास्त्र",
                "micros": [
                    (
                        "Matra_Varna_Scansion_Rules",
                        "मात्रा, वर्ण एवं गणना",
                    ),
                    (
                        "Matrik_Chhand_Doha_Soratha_Chaupai_Rola",
                        "मात्रिक छंद एवं प्रमुख उदाहरण",
                    ),
                ],
            },
            {
                "id": "ST10_03",
                "slug": "Alankara_Figures_of_Speech",
                "name": "अलंकार",
                "micros": [
                    (
                        "Shabdalankara_Anupras_Yamak_Shlesh",
                        "शब्दालंकार",
                    ),
                    (
                        "Arthalankara_Upama_Rupak_Utpreksha_Atishayokti",
                        "अर्थालंकार",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T11",
        "slug": "Linguistics_and_Hindi_Dialects",
        "title": "भाषा का उद्भव, बोलियाँ एवं देवनागरी लिपि",
        "subtopics": [
            {
                "id": "ST11_01",
                "slug": "Evolution_and_Dialects",
                "name": "भाषा विकास एवं क्षेत्रीय विविधता",
                "micros": [
                    (
                        "Apabhramsha_to_Modern_Languages",
                        "भाषा विकास की प्रमुख अवस्थाएँ",
                    ),
                    (
                        "Hindi_Dialects_and_Variation",
                        "हिन्दी की बोलियाँ एवं भाषाई विविधता",
                    ),
                ],
            },
            {
                "id": "ST11_02",
                "slug": "Devanagari_and_Official_Hindi",
                "name": "देवनागरी एवं राजभाषा हिन्दी",
                "micros": [
                    (
                        "Devanagari_Features_and_Standardization",
                        "देवनागरी की विशेषताएँ एवं मानकीकरण",
                    ),
                    (
                        "Constitutional_Provisions_Articles_343_351",
                        "राजभाषा संबंधी संवैधानिक प्रावधान",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T12",
        "slug": "Hindi_Literature_Eras_Writers_Awards",
        "title": "हिंदी साहित्य — प्रमुख युग, रचनाएँ एवं पुरस्कार",
        "subtopics": [
            {
                "id": "ST12_01",
                "slug": "Literary_Eras_and_Trends",
                "name": "साहित्यिक युग एवं प्रवृत्तियाँ",
                "micros": [
                    (
                        "Adikaal_Bhaktikaal_Reetikaal",
                        "आदिकाल, भक्तिकाल एवं रीतिकाल",
                    ),
                    (
                        "Modern_Era_and_Major_Trends",
                        "आधुनिक काल एवं प्रमुख साहित्यिक प्रवृत्तियाँ",
                    ),
                ],
            },
            {
                "id": "ST12_02",
                "slug": "Major_Writers_and_Genres",
                "name": "प्रमुख साहित्यकार एवं विधाएँ",
                "micros": [
                    (
                        "Prominent_Poets_and_Writers",
                        "प्रमुख कवि एवं साहित्यकार",
                    ),
                    (
                        "Major_Prose_Genres",
                        "प्रमुख गद्य विधाएँ",
                    ),
                ],
            },
            {
                "id": "ST12_03",
                "slug": "Awards_and_Magazines",
                "name": "पुरस्कार एवं पत्र-पत्रिकाएँ",
                "micros": [
                    (
                        "Major_Literary_Awards",
                        "प्रमुख साहित्यिक पुरस्कार",
                    ),
                    (
                        "Historical_Hindi_Journals",
                        "प्रमुख ऐतिहासिक हिन्दी पत्र-पत्रिकाएँ",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T13",
        "slug": "Language_Learning_and_Acquisition",
        "title": "भाषा अधिगम एवं भाषा अर्जन",
        "subtopics": [
            {
                "id": "ST13_01",
                "slug": "Acquisition_vs_Learning",
                "name": "भाषा अर्जन एवं अधिगम",
                "micros": [
                    (
                        "Natural_L1_Acquisition_vs_Formal_L2_Learning",
                        "प्राकृतिक भाषा अर्जन एवं औपचारिक भाषा अधिगम",
                    ),
                    (
                        "Affective_Filter_and_Environmental_Factors",
                        "भावात्मक एवं पर्यावरणीय कारक",
                    ),
                ],
            },
            {
                "id": "ST13_02",
                "slug": "Theories_of_Language_Development",
                "name": "भाषा विकास के सिद्धांत",
                "micros": [
                    (
                        "Chomsky_LAD_Universal_Grammar",
                        "चॉम्स्की एवं भाषा अर्जन",
                    ),
                    (
                        "Skinner_Imitation_Reinforcement_Model",
                        "स्किनर एवं व्यवहारवादी दृष्टिकोण",
                    ),
                    (
                        "Piaget_vs_Vygotsky_Language_Development",
                        "पियाजे एवं वायगोत्स्की के दृष्टिकोण",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T14",
        "slug": "Principles_and_Methods_of_Language_Teaching",
        "title": "भाषा शिक्षण के सिद्धांत, सूत्र एवं उपागम",
        "subtopics": [
            {
                "id": "ST14_01",
                "slug": "Pedagogical_Principles_and_Maxims",
                "name": "भाषा शिक्षण के सिद्धांत एवं सूत्र",
                "micros": [
                    (
                        "Activity_Motivation_Individual_Difference_Principles",
                        "क्रियाशीलता, प्रेरणा एवं व्यक्तिगत भिन्नता",
                    ),
                    (
                        "Concrete_to_Abstract_Maxims",
                        "मूर्त से अमूर्त एवं अन्य शिक्षण सूत्र",
                    ),
                ],
            },
            {
                "id": "ST14_02",
                "slug": "Language_Teaching_Methods",
                "name": "भाषा शिक्षण की विधियाँ",
                "micros": [
                    (
                        "Grammar_Translation_vs_Direct_Method",
                        "व्याकरण-अनुवाद एवं प्रत्यक्ष विधि",
                    ),
                    (
                        "Communicative_Language_Teaching",
                        "संचारात्मक भाषा शिक्षण",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T15",
        "slug": "Language_Skills_LSRW_Development",
        "title": "भाषाई कौशल — सुनना, बोलना, पढ़ना, लिखना",
        "subtopics": [
            {
                "id": "ST15_01",
                "slug": "Listening_and_Speaking",
                "name": "सुनना एवं बोलना",
                "micros": [
                    (
                        "Listening_Comprehension_Strategies",
                        "श्रवण बोध की रणनीतियाँ",
                    ),
                    (
                        "Oral_Expression_Pronunciation_Defects",
                        "मौखिक अभिव्यक्ति एवं उच्चारण",
                    ),
                ],
            },
            {
                "id": "ST15_02",
                "slug": "Reading_Skills",
                "name": "पठन कौशल",
                "micros": [
                    (
                        "Oral_vs_Silent_Reading_Skimming_Scanning",
                        "सस्वर, मौन, स्किमिंग एवं स्कैनिंग",
                    ),
                    (
                        "Reading_Comprehension_and_Dyslexia",
                        "पठन बोध एवं पठन कठिनाइयाँ",
                    ),
                ],
            },
            {
                "id": "ST15_03",
                "slug": "Writing_Skills",
                "name": "लेखन कौशल",
                "micros": [
                    (
                        "Calligraphy_Dictation_Creative_Writing",
                        "लेखन, श्रुतलेख एवं सृजनात्मक लेखन",
                    ),
                    (
                        "Spelling_Correctness_and_Dysgraphia",
                        "वर्तनी शुद्धता एवं लेखन कठिनाइयाँ",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T16",
        "slug": "Multilingualism_and_Classroom_Diversity",
        "title": "बहुभाषिकता एवं भाषाई विविधता",
        "subtopics": [
            {
                "id": "ST16_01",
                "slug": "Multilingualism_as_Resource",
                "name": "बहुभाषिकता एक संसाधन के रूप में",
                "micros": [
                    (
                        "Asset_Based_Multilingual_Pedagogy",
                        "बहुभाषिकता आधारित समावेशी शिक्षण",
                    ),
                    (
                        "Mother_Tongue_Cognitive_Advantages",
                        "मातृभाषा एवं संज्ञानात्मक विकास",
                    ),
                ],
            },
            {
                "id": "ST16_02",
                "slug": "Diversity_Challenges_and_Inclusion",
                "name": "भाषाई विविधता एवं समावेशन",
                "micros": [
                    (
                        "L1_Interference_Remediation",
                        "प्रथम भाषा अंतरण एवं सुधार",
                    ),
                    (
                        "Socio_Cultural_Inclusion_in_Language_Class",
                        "भाषा कक्षा में सामाजिक-सांस्कृतिक समावेशन",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T17",
        "slug": "Grammar_Role_TLM_and_Textbooks",
        "title": "व्याकरण की भूमिका एवं शिक्षण सामग्री",
        "subtopics": [
            {
                "id": "ST17_01",
                "slug": "Grammar_in_Context",
                "name": "संदर्भ में व्याकरण शिक्षण",
                "micros": [
                    (
                        "Contextual_Grammar_vs_Rote_Rules",
                        "संदर्भित व्याकरण एवं रटने की प्रवृत्ति",
                    ),
                    (
                        "Inductive_vs_Deductive_Grammar_Teaching",
                        "आगमनात्मक एवं निगमनात्मक व्याकरण शिक्षण",
                    ),
                ],
            },
            {
                "id": "ST17_02",
                "slug": "TLM_and_Reading_Materials",
                "name": "शिक्षण-अधिगम सामग्री एवं पठन सामग्री",
                "micros": [
                    (
                        "Textbook_Design_and_Child_Literature",
                        "पाठ्यपुस्तक एवं बाल साहित्य",
                    ),
                    (
                        "Audio_Visual_Language_Resources",
                        "श्रव्य-दृश्य एवं डिजिटल भाषा संसाधन",
                    ),
                ],
            },
        ],
    },
    {
        "id": "T18",
        "slug": "Language_Assessment_Remedial_Teaching_Policies",
        "title": "भाषाई आकलन, मूल्यांकन एवं नीतियाँ",
        "subtopics": [
            {
                "id": "ST18_01",
                "slug": "Continuous_Assessment_in_Language",
                "name": "भाषा में सतत आकलन",
                "micros": [
                    (
                        "Formative_and_Summative_Language_Assessment",
                        "रचनात्मक एवं संकलनात्मक आकलन",
                    ),
                    (
                        "Language_Rubrics_Portfolios_Checklists",
                        "रूब्रिक, पोर्टफोलियो एवं चेकलिस्ट",
                    ),
                ],
            },
            {
                "id": "ST18_02",
                "slug": "Diagnostic_and_Remedial_Teaching",
                "name": "नैदानिक एवं उपचारात्मक शिक्षण",
                "micros": [
                    (
                        "Language_Error_Analysis_and_Diagnosis",
                        "भाषाई त्रुटि विश्लेषण एवं निदान",
                    ),
                    (
                        "Remedial_Intervention_Modules",
                        "उपचारात्मक हस्तक्षेप",
                    ),
                ],
            },
            {
                "id": "ST18_03",
                "slug": "NEP_2020_and_NCF_Language_Directives",
                "name": "NEP 2020 एवं NCF भाषा संबंधी दृष्टिकोण",
                "micros": [
                    (
                        "NEP_2020_FLN_and_Language",
                        "NEP 2020, FLN एवं भाषा",
                    ),
                    (
                        "NCF_Language_Frameworks",
                        "NCF के भाषा संबंधी ढाँचे",
                    ),
                ],
            },
        ],
    },
]


# Existing physical folder names are deliberately preserved.
# This mapping allows the normalized taxonomy to coexist with
# the current scaffold without renaming/deleting anything.

LEGACY_TOPIC_FOLDERS = {
    "T01": "Topic_01_Unseen_Comprehension_Prose_and_Poetry",
    "T02": "Topic_02_Phonetics_Alphabet_and_Orthography",
    "T03": "Topic_03_Etymology_Word_Formation_Vocabulary",
    "T04": "Topic_04_Sandhi_Rules_and_Classification_UPTET",
    "T05": "Topic_05_Samas_Compound_Words_UPTET",
    "T06": "Topic_06_Parts_of_Speech_Declinable_Words",
    "T07": "Topic_07_Indeclinable_Words_Avyay_UPTET",
    "T08": "Topic_08_Grammatical_Categories",
    "T09": "Topic_09_Syntax_and_Punctuation",
    "T10": "Topic_10_Poetics_Rasa_Chhand_Alankara_UPTET",
    "T11": "Topic_11_Linguistics_and_Hindi_Dialects_UPTET",
    "T12": "Topic_12_Hindi_Literature_Eras_Writers_Awards_UPTET",
    "T13": "Topic_13_Language_Learning_and_Acquisition_CTET",
    "T14": "Topic_14_Principles_and_Methods_of_Language_Teaching",
    "T15": "Topic_15_Language_Skills_LSRW_Development_CTET",
    "T16": "Topic_16_Multilingualism_and_Classroom_Diversity_CTET",
    "T17": "Topic_17_Grammar_Role_TLM_and_Textbooks",
    "T18": "Topic_18_Language_Assessment_Remedial_Teaching_Policies",
}


# Existing physical subtopic folder names.
# Only known legacy suffixes are preserved. No folder is renamed.

LEGACY_SUBTOPIC_FOLDERS = {
    ("T02", "ST02_01"):
        "Subtopic_01_Hindi_Alphabet_and_Sounds_UPTET",
    ("T02", "ST02_02"):
        "Subtopic_02_Articulation_and_Effort_UPTET",
    ("T03", "ST03_01"):
        "Subtopic_01_Word_Origins_UPTET",
    ("T03", "ST03_02"):
        "Subtopic_02_Semantic_Vocabulary",
    ("T04", "ST04_01"):
        "Subtopic_01_Swar_Sandhi",
    ("T04", "ST04_02"):
        "Subtopic_02_Vyanjan_Sandhi",
    ("T04", "ST04_03"):
        "Subtopic_03_Visarga_Sandhi",
    ("T05", "ST05_01"):
        "Subtopic_01_Avyayibhav_and_Tatpurush",
    ("T05", "ST05_02"):
        "Subtopic_02_Karmadharaya_Dvigu_Dvandva_Bahuvrihi",
    ("T13", "ST13_01"):
        "Subtopic_01_Acquisition_vs_Learning",
    ("T13", "ST13_02"):
        "Subtopic_02_Theories_of_Language_Development",
    ("T15", "ST15_01"):
        "Subtopic_01_Listening_and_Speaking",
    ("T15", "ST15_02"):
        "Subtopic_02_Reading_Skills",
    ("T15", "ST15_03"):
        "Subtopic_03_Writing_Skills",
    ("T16", "ST16_01"):
        "Subtopic_01_Multilingualism_as_Resource",
    ("T16", "ST16_02"):
        "Subtopic_02_Diversity_Challenges_and_Inclusion",
}


# ============================================================
# VALIDATION
# ============================================================

def validate_required(condition, message):
    if not condition:
        raise ValueError(message)


def validate_id(value, label):
    validate_required(
        isinstance(value, str) and ID_PATTERN.fullmatch(value),
        f"Invalid {label}: {value!r}",
    )


def validate_unique_ids(items, label):
    ids = [item["id"] for item in items]
    duplicates = sorted(
        {
            item_id
            for item_id in ids
            if ids.count(item_id) > 1
        }
    )

    validate_required(
        not duplicates,
        f"Duplicate {label} IDs: {duplicates}",
    )


def validate_syllabus():
    validate_required(
        len(HINDI_SYLLABUS) == 18,
        "Hindi taxonomy must contain exactly 18 topics.",
    )

    validate_unique_ids(HINDI_SYLLABUS, "topic")

    for topic in HINDI_SYLLABUS:
        validate_id(topic["id"], "topic ID")
        validate_required(topic.get("slug"), f"Missing slug for {topic['id']}")
        validate_required(topic.get("title"), f"Missing title for {topic['id']}")
        validate_required(
            topic.get("subtopics"),
            f"Missing subtopics for {topic['id']}",
        )

        validate_unique_ids(topic["subtopics"], f"{topic['id']} subtopic")

        for subtopic in topic["subtopics"]:
            validate_id(
                subtopic["id"],
                f"subtopic ID in {topic['id']}",
            )

            validate_required(
                subtopic.get("slug"),
                f"Missing subtopic slug: {subtopic['id']}",
            )

            validate_required(
                subtopic.get("name"),
                f"Missing subtopic name: {subtopic['id']}",
            )

            micros = subtopic.get("micros", [])

            validate_required(
                micros,
                f"Missing micro-topics: {subtopic['id']}",
            )

            micro_ids = [
                f"{subtopic['id']}_M{index:02d}"
                for index, _ in enumerate(micros, start=1)
            ]

            validate_required(
                len(micro_ids) == len(set(micro_ids)),
                f"Duplicate generated micro IDs: {subtopic['id']}",
            )


# ============================================================
# JSON HELPERS
# ============================================================

def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def atomic_write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )
            file.write("\n")

        os.replace(temp_name, path)

    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


# ============================================================
# SCAFFOLD HELPERS
# ============================================================

def create_placeholder_markdown(path, title):
    if path.exists():
        return False

    path.write_text(
        f"# {title}\n\n"
        "*विषयवस्तु संकलन प्रगति पर है।*\n",
        encoding="utf-8",
    )

    return True


def create_placeholder_json(path, micro_topic_id, asset_type):
    if path.exists():
        return False

    data = {
        "micro_topic_id": micro_topic_id,
        "type": asset_type,
        "total_questions": 0,
        "questions": [],
    }

    atomic_write_json(path, data)
    return True


def ensure_asset_scaffold(
    micro_path,
    micro_topic_id,
    micro_title,
):
    created_dirs = 0
    created_files = 0

    for asset in LEAF_ASSETS:
        asset_path = micro_path / asset

        if not asset_path.exists():
            asset_path.mkdir(parents=True, exist_ok=True)
            created_dirs += 1

        if asset in ("Concept", "Short_Notes", "Practice"):
            target = asset_path / "content.md"

            if create_placeholder_markdown(
                target,
                micro_title,
            ):
                created_files += 1

        elif asset in ("MCQ", "PYQ"):
            target = asset_path / "content.json"

            if create_placeholder_json(
                target,
                micro_topic_id,
                asset,
            ):
                created_files += 1

    return created_dirs, created_files


# ============================================================
# EXISTING FOLDER RESOLUTION
# ============================================================

def resolve_topic_folder(topic):
    legacy = LEGACY_TOPIC_FOLDERS.get(topic["id"])

    if legacy:
        return legacy

    return (
        f"Topic_{topic['id'][1:]}_{topic['slug']}"
    )


def resolve_subtopic_folder(topic, subtopic, index):
    legacy = LEGACY_SUBTOPIC_FOLDERS.get(
        (topic["id"], subtopic["id"])
    )

    if legacy:
        return legacy

    return (
        f"Subtopic_{index:02d}_{subtopic['slug']}"
    )


def resolve_micro_folder(subtopic, micro_slug, index):
    return (
        f"Micro_{index:02d}_{micro_slug}"
    )


# ============================================================
# MANIFEST CONSTRUCTION
# ============================================================

def build_subject_manifest():
    topics = []

    total_subtopics = 0
    total_microtopics = 0

    for topic in HINDI_SYLLABUS:
        topic_folder = resolve_topic_folder(topic)

        topic_entry = {
            "id": topic["id"],
            "slug": topic["slug"],
            "name_hi": topic["title"],
            "folder": topic_folder,
            "order": int(topic["id"][1:]),
            "subtopics": [],
        }

        for sub_index, subtopic in enumerate(
            topic["subtopics"],
            start=1,
        ):
            subtopic_folder = resolve_subtopic_folder(
                topic,
                subtopic,
                sub_index,
            )

            subtopic_entry = {
                "id": subtopic["id"],
                "slug": subtopic["slug"],
                "name_hi": subtopic["name"],
                "folder": subtopic_folder,
                "order": sub_index,
                "micro_topics": [],
            }

            total_subtopics += 1

            for micro_index, micro_data in enumerate(
                subtopic["micros"],
                start=1,
            ):
                micro_slug, micro_title = micro_data

                micro_id = (
                    f"{subtopic['id']}_M{micro_index:02d}"
                )

                micro_folder = resolve_micro_folder(
                    subtopic,
                    micro_slug,
                    micro_index,
                )

                micro_entry = {
                    "id": micro_id,
                    "slug": micro_slug,
                    "name_hi": micro_title,
                    "folder": micro_folder,
                    "order": micro_index,
                    "assets": LEAF_ASSETS,
                }

                subtopic_entry["micro_topics"].append(
                    micro_entry
                )

                total_microtopics += 1

            topic_entry["subtopics"].append(
                subtopic_entry
            )

        topics.append(topic_entry)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "content_version": CONTENT_VERSION,
        "taxonomy_version": TAXONOMY_VERSION,

        "subject": {
            "id": SUBJECT_ID,
            "type": SUBJECT_TYPE,
            "name_en": SUBJECT_NAME_EN,
            "name_hi": SUBJECT_NAME_HI,
        },

        "status": STATUS,

        "exam_scope": EXAM_SCOPE,
        "paper_scope": PAPER_SCOPE,

        "asset_types": LEAF_ASSETS,

        "total_topics": len(topics),
        "total_subtopics": total_subtopics,
        "total_microtopics": total_microtopics,

        "topics": topics,
    }

    return manifest


# ============================================================
# MASTER MANIFEST RECONCILIATION
# ============================================================

def reconcile_master_manifest():
    validate_required(
        MASTER_MANIFEST.exists(),
        f"Master manifest not found: {MASTER_MANIFEST}",
    )

    master = load_json(MASTER_MANIFEST)

    validate_required(
        isinstance(master, dict),
        "Master manifest must be a JSON object.",
    )

    subjects = master.setdefault("subjects", [])

    hindi_entry = None

    for subject in subjects:
        if subject.get("id") == SUBJECT_ID:
            hindi_entry = subject
            break

    if hindi_entry is None:
        hindi_entry = {
            "id": SUBJECT_ID,
        }
        subjects.append(hindi_entry)

    # Preserve existing unknown fields.
    hindi_entry.update(
        {
            "id": SUBJECT_ID,
            "name_en": SUBJECT_NAME_EN,
            "name_hi": SUBJECT_NAME_HI,
            "directory": "Hindi",
            "manifest_path": "Hindi/manifest.json",
            "status": STATUS,
            "total_topics": len(HINDI_SYLLABUS),
            "framework_version": FRAMEWORK_VERSION,
            "taxonomy_version": TAXONOMY_VERSION,
        }
    )

    # Do NOT derive active_subjects_count from "ready".
    # That field belongs to a later publication/availability
    # contract and should not be changed by a scaffold generator.

    atomic_write_json(MASTER_MANIFEST, master)

    return master


# ============================================================
# FINAL VERIFICATION
# ============================================================

def verify_subject_manifest(manifest):
    validate_required(
        manifest["subject"]["id"] == SUBJECT_ID,
        "Subject ID mismatch.",
    )

    validate_required(
        manifest["status"] == STATUS,
        "Hindi status mismatch.",
    )

    validate_required(
        manifest["total_topics"] == 18,
        "Hindi topic count mismatch.",
    )

    validate_required(
        len(manifest["topics"]) == 18,
        "Hindi topic entries mismatch.",
    )

    validate_unique_ids(
        manifest["topics"],
        "manifest topic",
    )

    subtopic_count = 0
    micro_count = 0

    for topic in manifest["topics"]:
        subtopics = topic["subtopics"]

        validate_unique_ids(
            subtopics,
            f"{topic['id']} manifest subtopic",
        )

        subtopic_count += len(subtopics)

        for subtopic in subtopics:
            micros = subtopic["micro_topics"]

            micro_ids = [
                micro["id"]
                for micro in micros
            ]

            validate_required(
                len(micro_ids) == len(set(micro_ids)),
                f"Duplicate micro ID in {subtopic['id']}",
            )

            micro_count += len(micros)

    validate_required(
        subtopic_count == manifest["total_subtopics"],
        "Subtopic total mismatch.",
    )

    validate_required(
        micro_count == manifest["total_microtopics"],
        "Micro-topic total mismatch.",
    )

    validate_required(
        manifest["asset_types"] == LEAF_ASSETS,
        "Asset contract mismatch.",
    )

    return subtopic_count, micro_count


def verify_master_manifest():
    master = load_json(MASTER_MANIFEST)

    hindi_entries = [
        subject
        for subject in master.get("subjects", [])
        if subject.get("id") == SUBJECT_ID
    ]

    validate_required(
        len(hindi_entries) == 1,
        "Master manifest must contain exactly one HINDI entry.",
    )

    hindi = hindi_entries[0]

    validate_required(
        hindi.get("status") == STATUS,
        "Master HINDI status mismatch.",
    )

    validate_required(
        hindi.get("total_topics") == 18,
        "Master HINDI topic count mismatch.",
    )

    validate_required(
        hindi.get("manifest_path")
        == "Hindi/manifest.json",
        "Master HINDI manifest path mismatch.",
    )


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("SISKILL — HINDI FRAMEWORK GENERATOR")
    print("=" * 60)
    print(f"Subject ID       : {SUBJECT_ID}")
    print(f"Subject          : {SUBJECT_NAME_EN}")
    print(f"Framework        : {FRAMEWORK_VERSION}")
    print(f"Taxonomy         : {TAXONOMY_VERSION}")
    print(f"Status           : {STATUS}")
    print()

    print("1. Validating Hindi taxonomy...")
    validate_syllabus()

    print(
        f"   OK — {len(HINDI_SYLLABUS)} topics validated."
    )

    print("2. Reconciling Hindi directory scaffold...")

    BASE_PATH.mkdir(parents=True, exist_ok=True)

    created_dirs = 0
    created_files = 0

    for topic in HINDI_SYLLABUS:
        topic_folder = resolve_topic_folder(topic)
        topic_path = BASE_PATH / topic_folder

        if not topic_path.exists():
            topic_path.mkdir(
                parents=True,
                exist_ok=True,
            )
            created_dirs += 1

        for sub_index, subtopic in enumerate(
            topic["subtopics"],
            start=1,
        ):
            subtopic_folder = resolve_subtopic_folder(
                topic,
                subtopic,
                sub_index,
            )

            subtopic_path = topic_path / subtopic_folder

            if not subtopic_path.exists():
                subtopic_path.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                created_dirs += 1

            for micro_index, micro_data in enumerate(
                subtopic["micros"],
                start=1,
            ):
                micro_slug, micro_title = micro_data

                micro_id = (
                    f"{subtopic['id']}_M{micro_index:02d}"
                )

                micro_folder = resolve_micro_folder(
                    subtopic,
                    micro_slug,
                    micro_index,
                )

                micro_path = (
                    subtopic_path / micro_folder
                )

                if not micro_path.exists():
                    micro_path.mkdir(
                        parents=True,
                        exist_ok=True,
                    )
                    created_dirs += 1

                new_dirs, new_files = ensure_asset_scaffold(
                    micro_path,
                    micro_id,
                    micro_title,
                )

                created_dirs += new_dirs
                created_files += new_files

    print(
        f"   OK — existing scaffold preserved."
    )
    print(
        f"   New directories : {created_dirs}"
    )
    print(
        f"   New files       : {created_files}"
    )

    print("3. Building Hindi subject manifest...")

    manifest = build_subject_manifest()

    print("4. Writing Hindi subject manifest...")

    atomic_write_json(
        SUBJECT_MANIFEST,
        manifest,
    )

    print(
        f"   OK — {SUBJECT_MANIFEST}"
    )

    print("5. Reconciling master manifest...")

    reconcile_master_manifest()

    print(
        "   Existing HINDI entry reconciled."
    )

    print("6. Running final verification...")

    written_manifest = load_json(SUBJECT_MANIFEST)

    subtopic_count, micro_count = (
        verify_subject_manifest(
            written_manifest
        )
    )

    verify_master_manifest()

    print()
    print("=" * 60)
    print("HINDI FRAMEWORK GENERATION COMPLETE")
    print("=" * 60)
    print(
        f"Topics       : {written_manifest['total_topics']}"
    )
    print(
        f"Subtopics    : {subtopic_count}"
    )
    print(
        f"MicroTopics  : {micro_count}"
    )
    print(
        f"Asset Types  : {len(LEAF_ASSETS)}"
    )
    print(
        f"Status       : {STATUS}"
    )
    print()
    print("Subject manifest:")
    print(f"  {SUBJECT_MANIFEST}")
    print()
    print("Master manifest:")
    print(f"  {MASTER_MANIFEST}")
    print()
    print(
        "Existing directories/files were not deleted."
    )
    print("=" * 60)


if __name__ == "__main__":
    main()

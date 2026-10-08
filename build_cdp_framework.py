import json
import os
import re
from pathlib import Path


# ============================================================
# SISKILL — CDP FRAMEWORK GENERATOR
# Production-grade non-destructive scaffold generator
# ============================================================


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_PATH = "UPTET_CTET/Paper_1_and_2/Child_Development_and_Pedagogy"

MASTER_MANIFEST = (
    "UPTET_CTET/Paper_1_and_2/master_manifest.json"
)

SUBJECT_MANIFEST = os.path.join(
    BASE_PATH,
    "manifest.json",
)


# ------------------------------------------------------------
# FRAMEWORK METADATA
# ------------------------------------------------------------

FRAMEWORK_VERSION = "1.0.0"
CONTENT_VERSION = "0.1.0"
TAXONOMY_VERSION = "1.0.0"

SUBJECT_ID = "CDP"
SUBJECT_TYPE = "pedagogy"

SUBJECT_NAME_EN = "Child Development and Pedagogy"
SUBJECT_NAME_HI = "बाल विकास एवं शिक्षण शास्त्र"

EXAM_SCOPE = [
    "UPTET",
    "CTET",
]

PAPER_SCOPE = [
    "Paper_1",
    "Paper_2",
]

STATUS = "scaffolded"


# ------------------------------------------------------------
# CURRENT SCAFFOLD ASSETS
#
# IMPORTANT:
# This is intentionally NOT the final universal asset contract.
# The complete six-subject audit will define the final contract.
# ------------------------------------------------------------

LEAF_ASSETS = [
    "Concept",
    "Short_Notes",
    "PYQ",
    "MCQ",
    "Practice",
]


# ============================================================
# CDP TAXONOMY
# ============================================================

SYLLABUS = [

    {
        "id": "T01",
        "topic": "Growth_and_Development_Concepts",
        "title": "वृद्धि एवं विकास की संकल्पना",
        "subtopics": [
            {
                "id": "T01_ST01",
                "name": "Meaning_and_Definitions",
                "micros": [
                    "Growth_Meaning",
                    "Development_Meaning",
                    "Growth_vs_Development",
                    "Developmental_Change",
                ],
            },
            {
                "id": "T01_ST02",
                "name": "Principles_of_Development",
                "micros": [
                    "Development_Is_Continuous",
                    "Development_Follows_Sequence",
                    "Individual_Differences",
                    "General_to_Specific_Development",
                ],
            },
        ],
    },

    {
        "id": "T02",
        "topic": "Stages_and_Developmental_Tasks",
        "title": "विकास की अवस्थाएं एवं विकासात्मक कार्य",
        "subtopics": [
            {
                "id": "T02_ST01",
                "name": "Stages_of_Development",
                "micros": [
                    "Infancy",
                    "Early_Childhood",
                    "Middle_Childhood",
                    "Adolescence",
                ],
            },
            {
                "id": "T02_ST02",
                "name": "Developmental_Tasks",
                "micros": [
                    "Havighurst_Developmental_Tasks",
                    "Age_Specific_Tasks",
                    "Developmental_Readiness",
                ],
            },
        ],
    },

    {
        "id": "T03",
        "topic": "Heredity_and_Environment",
        "title": "वंशानुक्रम एवं वातावरण",
        "subtopics": [
            {
                "id": "T03_ST01",
                "name": "Heredity",
                "micros": [
                    "Meaning_of_Heredity",
                    "Genetic_Influence",
                    "Laws_of_Heredity",
                ],
            },
            {
                "id": "T03_ST02",
                "name": "Environment",
                "micros": [
                    "Meaning_of_Environment",
                    "Family_Environment",
                    "School_Environment",
                    "Social_Environment",
                ],
            },
            {
                "id": "T03_ST03",
                "name": "Heredity_Environment_Interaction",
                "micros": [
                    "Nature_Nurture_Debate",
                    "Interaction_of_Heredity_and_Environment",
                    "Educational_Implications",
                ],
            },
        ],
    },

    {
        "id": "T04",
        "topic": "Socialization_Processes",
        "title": "समाजीकरण की प्रक्रियाएं",
        "subtopics": [
            {
                "id": "T04_ST01",
                "name": "Social_World_and_Children",
                "micros": [
                    "Family_and_Socialization",
                    "Peer_Group",
                    "School_and_Socialization",
                    "Culture_and_Socialization",
                ],
            },
            {
                "id": "T04_ST02",
                "name": "Agents_of_Socialization",
                "micros": [
                    "Parents",
                    "Teachers",
                    "Peers",
                    "Community",
                    "Media",
                ],
            },
        ],
    },

    {
        "id": "T05",
        "topic": "Cognitive_Theories_Piaget_Vygotsky_Bruner",
        "title": "संज्ञानात्मक विकास के सिद्धांत",
        "subtopics": [
            {
                "id": "T05_ST01",
                "name": "Piaget_Cognitive_Development",
                "micros": [
                    "Piaget_Theory_Overview",
                    "Sensorimotor_Stage",
                    "Preoperational_Stage",
                    "Concrete_Operational_Stage",
                    "Formal_Operational_Stage",
                    "Schema_Assimilation_Accommodation",
                ],
            },
            {
                "id": "T05_ST02",
                "name": "Vygotsky_Social_Cultural_Theory",
                "micros": [
                    "Social_Cultural_Theory",
                    "Zone_of_Proximal_Development",
                    "More_Knowledgeable_Other",
                    "Scaffolding",
                    "Language_and_Thought",
                ],
            },
            {
                "id": "T05_ST03",
                "name": "Bruner_Cognitive_Theory",
                "micros": [
                    "Discovery_Learning",
                    "Modes_of_Representation",
                    "Spiral_Curriculum",
                    "Scaffolding_in_Bruner",
                ],
            },
        ],
    },

    {
        "id": "T06",
        "topic": "Moral_Development_Theories",
        "title": "नैतिक विकास के सिद्धांत",
        "subtopics": [
            {
                "id": "T06_ST01",
                "name": "Kohlberg_Moral_Development",
                "micros": [
                    "Kohlberg_Theory",
                    "Preconventional_Level",
                    "Conventional_Level",
                    "Postconventional_Level",
                    "Moral_Dilemmas",
                ],
            },
            {
                "id": "T06_ST02",
                "name": "Piaget_Moral_Development",
                "micros": [
                    "Heteronomous_Morality",
                    "Autonomous_Morality",
                    "Moral_Reasoning",
                ],
            },
        ],
    },

    {
        "id": "T07",
        "topic": "Psychosocial_and_Psychoanalytic_Theories",
        "title": "मनोसामाजिक एवं मनोविश्लेषणात्मक सिद्धांत",
        "subtopics": [
            {
                "id": "T07_ST01",
                "name": "Erikson_Psychosocial_Theory",
                "micros": [
                    "Erikson_Theory",
                    "Psychosocial_Stages",
                    "Trust_vs_Mistrust",
                    "Autonomy_vs_Shame",
                    "Initiative_vs_Guilt",
                    "Industry_vs_Inferiority",
                    "Identity_vs_Role_Confusion",
                ],
            },
            {
                "id": "T07_ST02",
                "name": "Freud_Psychoanalysis",
                "micros": [
                    "Freud_Theory",
                    "Id_Ego_Superego",
                    "Psychosexual_Stages",
                    "Educational_Implications",
                ],
            },
        ],
    },

    {
        "id": "T08",
        "topic": "Language_and_Thought",
        "title": "भाषा एवं चिंतन",
        "subtopics": [
            {
                "id": "T08_ST01",
                "name": "Language_Development",
                "micros": [
                    "Language_Development_Stages",
                    "Language_Acquisition",
                    "Bilingualism",
                    "Multilingualism",
                ],
            },
            {
                "id": "T08_ST02",
                "name": "Language_Thought_Relationship",
                "micros": [
                    "Language_and_Cognition",
                    "Vygotsky_Language_Thought",
                    "Piaget_Language_Thought",
                ],
            },
        ],
    },

    {
        "id": "T09",
        "topic": "Cognition_Emotion_and_Motivation",
        "title": "संज्ञान, संवेग एवं अभिप्रेरणा",
        "subtopics": [
            {
                "id": "T09_ST01",
                "name": "Cognition",
                "micros": [
                    "Cognitive_Processes",
                    "Attention",
                    "Memory",
                    "Perception",
                ],
            },
            {
                "id": "T09_ST02",
                "name": "Emotion",
                "micros": [
                    "Meaning_of_Emotion",
                    "Emotional_Development",
                    "Emotional_Intelligence",
                ],
            },
            {
                "id": "T09_ST03",
                "name": "Motivation",
                "micros": [
                    "Intrinsic_Motivation",
                    "Extrinsic_Motivation",
                    "Achievement_Motivation",
                    "Teacher_Role_in_Motivation",
                ],
            },
        ],
    },

    {
        "id": "T10",
        "topic": "Personality_Theories_and_Assessment",
        "title": "व्यक्तित्व के सिद्धांत एवं मापन",
        "subtopics": [
            {
                "id": "T10_ST01",
                "name": "Personality_Concept",
                "micros": [
                    "Meaning_of_Personality",
                    "Characteristics_of_Personality",
                    "Determinants_of_Personality",
                ],
            },
            {
                "id": "T10_ST02",
                "name": "Personality_Theories",
                "micros": [
                    "Trait_Theory",
                    "Type_Theory",
                    "Psychoanalytic_View",
                    "Humanistic_View",
                ],
            },
            {
                "id": "T10_ST03",
                "name": "Personality_Assessment",
                "micros": [
                    "Objective_Tests",
                    "Projective_Tests",
                    "Observation_Method",
                    "Interview_Method",
                ],
            },
        ],
    },

    {
        "id": "T11",
        "topic": "Intelligence_Theories_and_Testing",
        "title": "बुद्धि के सिद्धांत एवं परीक्षण",
        "subtopics": [
            {
                "id": "T11_ST01",
                "name": "Intelligence_Concept",
                "micros": [
                    "Meaning_of_Intelligence",
                    "Nature_of_Intelligence",
                    "Intelligence_and_Learning",
                ],
            },
            {
                "id": "T11_ST02",
                "name": "Intelligence_Theories",
                "micros": [
                    "Spearman_Two_Factor_Theory",
                    "Thurstone_Primary_Mental_Abilities",
                    "Guilford_Structure_of_Intellect",
                    "Gardner_Multiple_Intelligences",
                    "Sternberg_Triarchic_Theory",
                ],
            },
            {
                "id": "T11_ST03",
                "name": "Intelligence_Testing",
                "micros": [
                    "IQ_Concept",
                    "Individual_Intelligence_Tests",
                    "Group_Intelligence_Tests",
                    "Verbal_and_Nonverbal_Tests",
                ],
            },
        ],
    },

    {
        "id": "T12",
        "topic": "Individual_Differences_and_Gender",
        "title": "व्यक्तिगत विभिन्नताएं एवं जेंडर",
        "subtopics": [
            {
                "id": "T12_ST01",
                "name": "Individual_Differences",
                "micros": [
                    "Meaning_of_Individual_Differences",
                    "Cognitive_Differences",
                    "Learning_Differences",
                    "Personality_Differences",
                ],
            },
            {
                "id": "T12_ST02",
                "name": "Gender_and_Education",
                "micros": [
                    "Gender_Roles",
                    "Gender_Stereotypes",
                    "Gender_Bias",
                    "Gender_Sensitive_Classroom",
                ],
            },
        ],
    },

    {
        "id": "T13",
        "topic": "Thinking_Problem_Solving_and_Creativity",
        "title": "चिंतन, समस्या समाधान एवं सृजनात्मकता",
        "subtopics": [
            {
                "id": "T13_ST01",
                "name": "Thinking",
                "micros": [
                    "Meaning_of_Thinking",
                    "Convergent_Thinking",
                    "Divergent_Thinking",
                    "Critical_Thinking",
                ],
            },
            {
                "id": "T13_ST02",
                "name": "Problem_Solving",
                "micros": [
                    "Problem_Solving_Process",
                    "Strategies_of_Problem_Solving",
                    "Teacher_Role",
                ],
            },
            {
                "id": "T13_ST03",
                "name": "Creativity",
                "micros": [
                    "Meaning_of_Creativity",
                    "Characteristics_of_Creative_Children",
                    "Creative_Thinking",
                    "Encouraging_Creativity",
                ],
            },
        ],
    },

    {
        "id": "T14",
        "topic": "Learning_Concepts_and_Laws",
        "title": "अधिगम की संकल्पना एवं नियम",
        "subtopics": [
            {
                "id": "T14_ST01",
                "name": "Learning_Concept",
                "micros": [
                    "Meaning_of_Learning",
                    "Characteristics_of_Learning",
                    "Factors_Affecting_Learning",
                ],
            },
            {
                "id": "T14_ST02",
                "name": "Laws_of_Learning",
                "micros": [
                    "Thorndike_Laws",
                    "Law_of_Readiness",
                    "Law_of_Exercise",
                    "Law_of_Effect",
                ],
            },
        ],
    },

    {
        "id": "T15",
        "topic": "Learning_Theories_and_Pedagogy",
        "title": "अधिगम के सिद्धांत एवं शिक्षाशास्त्र",
        "subtopics": [
            {
                "id": "T15_ST01",
                "name": "Behaviorist_Conditioning",
                "micros": [
                    "Classical_Conditioning",
                    "Pavlov",
                    "Operant_Conditioning",
                    "Skinner",
                    "Reinforcement_and_Punishment",
                ],
            },
            {
                "id": "T15_ST02",
                "name": "Cognitive_Learning",
                "micros": [
                    "Insight_Learning",
                    "Gestalt_Learning",
                    "Cognitive_Maps",
                ],
            },
            {
                "id": "T15_ST03",
                "name": "Constructivist_Learning",
                "micros": [
                    "Constructivism",
                    "Learner_Centered_Learning",
                    "Active_Learning",
                    "Collaborative_Learning",
                ],
            },
        ],
    },

    {
        "id": "T16",
        "topic": "Teaching_Methods_Skills_and_Models",
        "title": "शिक्षण विधियां, कौशल एवं मॉडल",
        "subtopics": [
            {
                "id": "T16_ST01",
                "name": "Teaching_Methods",
                "micros": [
                    "Lecture_Method",
                    "Discussion_Method",
                    "Project_Method",
                    "Demonstration_Method",
                    "Problem_Solving_Method",
                ],
            },
            {
                "id": "T16_ST02",
                "name": "Teaching_Skills",
                "micros": [
                    "Questioning_Skill",
                    "Explanation_Skill",
                    "Reinforcement_Skill",
                    "Stimulus_Variation",
                ],
            },
            {
                "id": "T16_ST03",
                "name": "Teaching_Models",
                "micros": [
                    "Advance_Organizer_Model",
                    "Concept_Attainment_Model",
                    "Inquiry_Model",
                ],
            },
        ],
    },

    {
        "id": "T17",
        "topic": "Inclusive_Education_Philosophy",
        "title": "समावेशी शिक्षा का दर्शन",
        "subtopics": [
            {
                "id": "T17_ST01",
                "name": "Inclusive_Education",
                "micros": [
                    "Meaning_of_Inclusion",
                    "Principles_of_Inclusion",
                    "Inclusive_Classroom",
                    "Teacher_Role",
                ],
            },
            {
                "id": "T17_ST02",
                "name": "Diversity_in_Classroom",
                "micros": [
                    "Cultural_Diversity",
                    "Linguistic_Diversity",
                    "Socioeconomic_Diversity",
                    "Learning_Diversity",
                ],
            },
        ],
    },

    {
        "id": "T18",
        "topic": "Learning_Disabilities_and_Neurodiversity",
        "title": "अधिगम अक्षमताएं एवं न्यूरोडायवर्सिटी",
        "subtopics": [
            {
                "id": "T18_ST01",
                "name": "Learning_Disabilities",
                "micros": [
                    "Dyslexia",
                    "Dysgraphia",
                    "Dyscalculia",
                    "Specific_Learning_Disability",
                ],
            },
            {
                "id": "T18_ST02",
                "name": "Neurodevelopmental_Conditions",
                "micros": [
                    "Autism_Spectrum",
                    "ADHD",
                    "Intellectual_Disability",
                    "Educational_Support",
                ],
            },
        ],
    },

    {
        "id": "T19",
        "topic": "RPwD_Act_2016_and_Exceptional_Children",
        "title": "RPwD अधिनियम 2016 एवं विशेष आवश्यकता वाले बच्चे",
        "subtopics": [
            {
                "id": "T19_ST01",
                "name": "RPwD_Act_2016",
                "micros": [
                    "RPwD_Act_2016_Overview",
                    "Rights_and_Entitlements",
                    "Inclusive_Education_Provisions",
                    "Reasonable_Accommodation",
                ],
            },
            {
                "id": "T19_ST02",
                "name": "Exceptional_Children",
                "micros": [
                    "Gifted_Children",
                    "Children_with_Disabilities",
                    "Slow_Learners",
                    "Educational_Adaptations",
                ],
            },
        ],
    },

    {
        "id": "T20",
        "topic": "Guidance_Counselling_and_UP_Agencies",
        "title": "निर्देशन, परामर्श एवं उत्तर प्रदेश की शैक्षिक संस्थाएं",
        "subtopics": [
            {
                "id": "T20_ST01",
                "name": "Guidance",
                "micros": [
                    "Meaning_of_Guidance",
                    "Types_of_Guidance",
                    "Principles_of_Guidance",
                ],
            },
            {
                "id": "T20_ST02",
                "name": "Counselling",
                "micros": [
                    "Meaning_of_Counselling",
                    "Counselling_Process",
                    "Teacher_as_Counsellor",
                ],
            },
            {
                "id": "T20_ST03",
                "name": "Educational_Agencies",
                "micros": [
                    "SCERT",
                    "DIET",
                    "NCERT",
                    "NCTE",
                ],
            },
        ],
    },

    {
        "id": "T21",
        "topic": "Measurement_Assessment_and_Evaluation",
        "title": "मापन, आकलन एवं मूल्यांकन",
        "subtopics": [
            {
                "id": "T21_ST01",
                "name": "Measurement",
                "micros": [
                    "Meaning_of_Measurement",
                    "Characteristics_of_Measurement",
                    "Quantitative_Measurement",
                ],
            },
            {
                "id": "T21_ST02",
                "name": "Assessment",
                "micros": [
                    "Assessment_for_Learning",
                    "Assessment_of_Learning",
                    "Formative_Assessment",
                    "Summative_Assessment",
                ],
            },
            {
                "id": "T21_ST03",
                "name": "Evaluation",
                "micros": [
                    "Meaning_of_Evaluation",
                    "Diagnostic_Evaluation",
                    "Continuous_Assessment",
                ],
            },
        ],
    },

    {
        "id": "T22",
        "topic": "Test_Standardization_and_Action_Research",
        "title": "परीक्षण मानकीकरण एवं क्रियात्मक अनुसंधान",
        "subtopics": [
            {
                "id": "T22_ST01",
                "name": "Test_Standardization",
                "micros": [
                    "Validity",
                    "Reliability",
                    "Objectivity",
                    "Norms",
                ],
            },
            {
                "id": "T22_ST02",
                "name": "Action_Research",
                "micros": [
                    "Meaning_of_Action_Research",
                    "Steps_of_Action_Research",
                    "Teacher_as_Researcher",
                ],
            },
        ],
    },

    {
        "id": "T23",
        "topic": "NEP_2020_and_NCF_Frameworks",
        "title": "राष्ट्रीय शिक्षा नीति 2020 एवं NCF ढांचे",
        "subtopics": [
            {
                "id": "T23_ST01",
                "name": "NEP_2020",
                "micros": [
                    "NEP_2020_Overview",
                    "Foundational_Literacy_and_Numeracy",
                    "School_Education_Structure",
                    "Competency_Based_Education",
                ],
            },
            {
                "id": "T23_ST02",
                "name": "NCF_Frameworks",
                "micros": [
                    "NCF_Overview",
                    "Curriculum_Principles",
                    "Child_Centered_Education",
                ],
            },
        ],
    },

    {
        "id": "T24",
        "topic": "RTE_Act_2009_and_Child_Rights",
        "title": "RTE अधिनियम 2009 एवं बाल अधिकार",
        "subtopics": [
            {
                "id": "T24_ST01",
                "name": "RTE_Act_2009",
                "micros": [
                    "RTE_Act_Overview",
                    "Right_to_Free_and_Compulsory_Education",
                    "School_Responsibilities",
                    "Teacher_Responsibilities",
                ],
            },
            {
                "id": "T24_ST02",
                "name": "Child_Rights",
                "micros": [
                    "Child_Rights_Concept",
                    "Protection_of_Children",
                    "Child_Centered_Education",
                ],
            },
        ],
    },

    {
        "id": "T25",
        "topic": "Historical_Evolution_of_Indian_Education",
        "title": "भारतीय शिक्षा का ऐतिहासिक विकास",
        "subtopics": [
            {
                "id": "T25_ST01",
                "name": "Ancient_Indian_Education",
                "micros": [
                    "Gurukul_System",
                    "Buddhist_Education",
                    "Medieval_Education",
                ],
            },
            {
                "id": "T25_ST02",
                "name": "Modern_Indian_Education",
                "micros": [
                    "Wood_Despatch",
                    "Hunter_Commission",
                    "Sadler_Commission",
                    "Wardha_Scheme",
                ],
            },
            {
                "id": "T25_ST03",
                "name": "Post_Independence_Education",
                "micros": [
                    "Kothari_Commission",
                    "National_Policy_on_Education_1968",
                    "National_Policy_on_Education_1986",
                ],
            },
        ],
    },

    {
        "id": "T26",
        "topic": "Philosophical_Schools_and_Thinkers",
        "title": "दार्शनिक विचारधाराएं एवं शिक्षाविद",
        "subtopics": [
            {
                "id": "T26_ST01",
                "name": "Indian_Philosophers",
                "micros": [
                    "Swami_Vivekananda",
                    "Mahatma_Gandhi",
                    "Rabindranath_Tagore",
                    "Sri_Aurobindo",
                ],
            },
            {
                "id": "T26_ST02",
                "name": "Western_Philosophers",
                "micros": [
                    "Socrates",
                    "Plato",
                    "Aristotle",
                    "John_Dewey",
                    "Rousseau",
                ],
            },
            {
                "id": "T26_ST03",
                "name": "Educational_Philosophy",
                "micros": [
                    "Idealism",
                    "Naturalism",
                    "Pragmatism",
                    "Realism",
                ],
            },
        ],
    },

    {
        "id": "T27",
        "topic": "National_Schemes_and_UP_Structure_UPTET",
        "title": "प्रारंभिक शिक्षा की प्रमुख योजनाएं एवं संस्थागत संरचना",
        "subtopics": [
            {
                "id": "T27_ST01",
                "name": "National_Education_Schemes",
                "micros": [
                    "Mid_Day_Meal",
                    "Samagra_Shiksha",
                    "Sarva_Shiksha_Abhiyan",
                    "NIPUN_Bharat",
                ],
            },
            {
                "id": "T27_ST02",
                "name": "UP_Education_Structure",
                "micros": [
                    "Basic_Education_Department",
                    "DIET_Structure",
                    "SCERT_Uttar_Pradesh",
                    "UP_Exam_Authorities",
                ],
            },
        ],
    },
]


# ============================================================
# VALIDATION
# ============================================================

ID_PATTERN = re.compile(r"^[A-Z0-9_]+$")


def validate_required(value, field_name):
    """Validate that a required field is not empty."""

    if value is None or str(value).strip() == "":
        raise ValueError(
            f"Required field is empty: {field_name}"
        )


def validate_id(value, field_name):
    """Validate stable framework IDs."""

    validate_required(value, field_name)

    if not ID_PATTERN.fullmatch(str(value)):
        raise ValueError(
            f"Invalid ID '{value}' in {field_name}. "
            "Allowed characters: A-Z, 0-9 and underscore."
        )


def validate_unique_ids(items, field_name):
    """Detect duplicate IDs."""

    seen = set()

    for item in items:

        item_id = item.get("id")

        if item_id in seen:
            raise ValueError(
                f"Duplicate {field_name} ID detected: "
                f"{item_id}"
            )

        seen.add(item_id)


def validate_syllabus():
    """
    Validate the CDP taxonomy before filesystem mutation.

    This validates structural integrity only.
    It does not claim that every taxonomy item is an
    officially mapped UPTET/CTET syllabus item.
    """

    if not isinstance(SYLLABUS, list):
        raise TypeError(
            "SYLLABUS must be a list."
        )

    if not SYLLABUS:
        raise ValueError(
            "SYLLABUS cannot be empty."
        )

    validate_unique_ids(
        SYLLABUS,
        "topic"
    )

    for topic in SYLLABUS:

        validate_id(
            topic.get("id"),
            "topic"
        )

        validate_required(
            topic.get("topic"),
            f"topic {topic.get('id')} slug"
        )

        validate_required(
            topic.get("title"),
            f"topic {topic.get('id')} title"
        )

        subtopics = topic.get("subtopics")

        if not isinstance(subtopics, list):
            raise TypeError(
                f"Subtopics for {topic.get('id')} "
                "must be a list."
            )

        if not subtopics:
            raise ValueError(
                f"Topic {topic.get('id')} "
                "has no subtopics."
            )

        validate_unique_ids(
            subtopics,
            f"subtopic under {topic.get('id')}"
        )

        for subtopic in subtopics:

            validate_id(
                subtopic.get("id"),
                f"subtopic under {topic.get('id')}"
            )

            validate_required(
                subtopic.get("name"),
                f"subtopic {subtopic.get('id')} name"
            )

            micros = subtopic.get("micros")

            if not isinstance(micros, list):
                raise TypeError(
                    f"Micro topics for "
                    f"{subtopic.get('id')} "
                    "must be a list."
                )

            if not micros:
                raise ValueError(
                    f"Subtopic {subtopic.get('id')} "
                    "has no micro topics."
                )

            if len(micros) != len(set(micros)):
                raise ValueError(
                    f"Duplicate micro topic detected "
                    f"under {subtopic.get('id')}."
                )


# ============================================================
# JSON UTILITIES
# ============================================================

def load_json(path):
    """Load JSON from disk."""

    target = Path(path)

    if not target.exists():
        raise FileNotFoundError(
            f"Required JSON file does not exist: {path}"
        )

    with target.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def write_json_atomic(path, data):
    """
    Write JSON using a temporary file and atomic replacement.

    Existing target is replaced only after successful
    serialization.
    """

    target = Path(path)

    target.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = target.with_suffix(
        target.suffix + ".tmp"
    )

    with temporary.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

        file.write("\n")

    temporary.replace(target)


# ============================================================
# MAIN GENERATION
# ============================================================

def main():

    print()
    print("=" * 60)
    print("SISKILL — CDP FRAMEWORK GENERATOR")
    print("=" * 60)

    print(
        f"Subject ID       : {SUBJECT_ID}"
    )

    print(
        f"Subject          : {SUBJECT_NAME_EN}"
    )

    print(
        f"Framework        : {FRAMEWORK_VERSION}"
    )

    print(
        f"Taxonomy         : {TAXONOMY_VERSION}"
    )

    print(
        f"Status           : {STATUS}"
    )

    print()

    # --------------------------------------------------------
    # VALIDATION BEFORE MUTATION
    # --------------------------------------------------------

    print(
        "1. Validating CDP taxonomy..."
    )

    validate_syllabus()

    print(
        f"   OK — {len(SYLLABUS)} topics validated."
    )

    # --------------------------------------------------------
    # ROOT DIRECTORY
    # --------------------------------------------------------

    print(
        "2. Reconciling CDP directory scaffold..."
    )

    root_path = Path(BASE_PATH)

    root_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # SUBJECT MANIFEST
    # --------------------------------------------------------

    manifest_data = {

        "schema_version": "1.0.0",

        "framework_version":
            FRAMEWORK_VERSION,

        "content_version":
            CONTENT_VERSION,

        "taxonomy_version":
            TAXONOMY_VERSION,

        "status":
            STATUS,

        "exam_scope":
            EXAM_SCOPE,

        "paper_scope":
            PAPER_SCOPE,

        "subject": {

            "id":
                SUBJECT_ID,

            "type":
                SUBJECT_TYPE,

            "name_en":
                SUBJECT_NAME_EN,

            "name_hi":
                SUBJECT_NAME_HI,

            "directory":
                root_path.name,
        },

        "total_topics":
            len(SYLLABUS),

        "asset_types":
            LEAF_ASSETS,

        "topics": [],
    }

    # --------------------------------------------------------
    # TOPIC / SUBTOPIC / MICRO GENERATION
    # --------------------------------------------------------

    for topic_order, topic in enumerate(
        SYLLABUS,
        start=1
    ):

        topic_dir_name = (
            f"Topic_{topic_order:02d}_"
            f"{topic['topic']}"
        )

        topic_path = (
            root_path / topic_dir_name
        )

        topic_path.mkdir(
            parents=True,
            exist_ok=True
        )

        topic_entry = {

            "id":
                topic["id"],

            "slug":
                topic["topic"],

            "title_hi":
                topic["title"],

            "order":
                topic_order,

            "folder":
                topic_dir_name,

            "subtopics": [],
        }

        for subtopic_order, subtopic in enumerate(
            topic["subtopics"],
            start=1
        ):

            subtopic_dir_name = (
                f"Subtopic_{subtopic_order:02d}_"
                f"{subtopic['name']}"
            )

            subtopic_path = (
                topic_path /
                subtopic_dir_name
            )

            subtopic_path.mkdir(
                parents=True,
                exist_ok=True
            )

            subtopic_entry = {

                "id":
                    subtopic["id"],

                "slug":
                    subtopic["name"],

                "order":
                    subtopic_order,

                "folder":
                    subtopic_dir_name,

                "micro_topics": [],
            }

            for micro_order, micro in enumerate(
                subtopic["micros"],
                start=1
            ):

                micro_dir_name = (
                    f"Micro_{micro_order:02d}_"
                    f"{micro}"
                )

                micro_path = (
                    subtopic_path /
                    micro_dir_name
                )

                micro_path.mkdir(
                    parents=True,
                    exist_ok=True
                )

                for asset in LEAF_ASSETS:

                    asset_path = (
                        micro_path / asset
                    )

                    asset_path.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                micro_id = (
                    f"{subtopic['id']}"
                    f"_M{micro_order:02d}"
                )

                subtopic_entry[
                    "micro_topics"
                ].append(
                    {
                        "id":
                            micro_id,

                        "slug":
                            micro,

                        "folder":
                            micro_dir_name,

                        "order":
                            micro_order,

                        "assets":
                            list(LEAF_ASSETS),
                    }
                )

            topic_entry[
                "subtopics"
            ].append(
                subtopic_entry
            )

        manifest_data[
            "topics"
        ].append(
            topic_entry
        )

    # --------------------------------------------------------
    # WRITE SUBJECT MANIFEST
    # --------------------------------------------------------

    print(
        "3. Writing CDP subject manifest..."
    )

    write_json_atomic(
        SUBJECT_MANIFEST,
        manifest_data
    )

    print(
        f"   OK — {SUBJECT_MANIFEST}"
    )

    # --------------------------------------------------------
    # MASTER MANIFEST
    # --------------------------------------------------------

    print(
        "4. Reconciling master manifest..."
    )

    master = load_json(
        MASTER_MANIFEST
    )

    if not isinstance(master, dict):
        raise ValueError(
            "Master manifest root must be a JSON object."
        )

    subjects = master.setdefault(
        "subjects",
        []
    )

    if not isinstance(subjects, list):
        raise ValueError(
            "master_manifest.json 'subjects' "
            "must be a list."
        )

    cdp_entry = {

        "id":
            SUBJECT_ID,

        "name_en":
            SUBJECT_NAME_EN,

        "name_hi":
            SUBJECT_NAME_HI,

        "directory":
            root_path.name,

        "manifest_path":
            f"{root_path.name}/manifest.json",

        "status":
            STATUS,

        "total_topics":
            len(SYLLABUS),

        "framework_version":
            FRAMEWORK_VERSION,

        "taxonomy_version":
            TAXONOMY_VERSION,
    }

    existing_index = None

    for index, subject in enumerate(subjects):

        if subject.get("id") == SUBJECT_ID:

            existing_index = index
            break

    if existing_index is None:

        subjects.append(
            cdp_entry
        )

        print(
            "   CDP entry added."
        )

    else:

        # Preserve unknown/custom fields while updating
        # controlled CDP framework fields.
        subjects[existing_index] = {
            **subjects[existing_index],
            **cdp_entry,
        }

        print(
            "   Existing CDP entry reconciled."
        )

    master[
        "active_subjects_count"
    ] = len(subjects)

    master.setdefault(
        "total_planned_subjects",
        len(subjects)
    )

    write_json_atomic(
        MASTER_MANIFEST,
        master
    )

    # --------------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------------

    print(
        "5. Running final verification..."
    )

    verified_subject_manifest = load_json(
        SUBJECT_MANIFEST
    )

    verified_master_manifest = load_json(
        MASTER_MANIFEST
    )

    if (
        verified_subject_manifest
        .get("subject", {})
        .get("id")
        != SUBJECT_ID
    ):

        raise ValueError(
            "CDP subject manifest verification failed."
        )

    if (
        verified_subject_manifest
        .get("total_topics")
        != len(SYLLABUS)
    ):

        raise ValueError(
            "CDP topic count verification failed."
        )

    verified_cdp = next(
        (
            item
            for item in
            verified_master_manifest.get(
                "subjects",
                []
            )
            if item.get("id") == SUBJECT_ID
        ),
        None
    )

    if verified_cdp is None:

        raise ValueError(
            "CDP entry missing from master manifest."
        )

    expected_manifest_path = (
        f"{root_path.name}/manifest.json"
    )

    if (
        verified_cdp.get("manifest_path")
        != expected_manifest_path
    ):

        raise ValueError(
            "CDP manifest_path verification failed."
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    subtopic_count = sum(
        len(topic["subtopics"])
        for topic in SYLLABUS
    )

    micro_count = sum(
        len(subtopic["micros"])
        for topic in SYLLABUS
        for subtopic in topic["subtopics"]
    )

    print()
    print("=" * 60)
    print("CDP FRAMEWORK GENERATION COMPLETE")
    print("=" * 60)

    print(
        f"Topics       : {len(SYLLABUS)}"
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
    print(
        "Subject manifest:"
    )

    print(
        f"  {SUBJECT_MANIFEST}"
    )

    print()
    print(
        "Master manifest:"
    )

    print(
        f"  {MASTER_MANIFEST}"
    )

    print()
    print(
        "Existing directories/files were not deleted."
    )

    print(
        "============================================================"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()


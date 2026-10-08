import json
import os
import re
from pathlib import Path


# ============================================================
# SISKILL — MATH FRAMEWORK GENERATOR
# Production-grade scaffold reconciliation
# ============================================================

BASE_PATH = Path("UPTET_CTET/Paper_1_and_2/Mathematics")
MASTER_MANIFEST = Path("UPTET_CTET/Paper_1_and_2/master_manifest.json")
SUBJECT_MANIFEST = BASE_PATH / "manifest.json"

FRAMEWORK_VERSION = "1.0.0"
CONTENT_VERSION = "0.1.0"
TAXONOMY_VERSION = "1.0.0"

SUBJECT_ID = "MATH"
SUBJECT_TYPE = "mathematics_pedagogy"
SUBJECT_NAME_EN = "Mathematics and Pedagogy"
SUBJECT_NAME_HI = "गणित एवं शिक्षण शास्त्र"

EXAM_SCOPE = ["UPTET", "CTET"]
PAPER_SCOPE = ["Paper_1", "Paper_2"]

STATUS = "scaffolded"

# Universal asset contract is intentionally frozen at five assets
# until all six subject frameworks are audited.
LEAF_ASSETS = [
    "Concept",
    "Short_Notes",
    "PYQ",
    "MCQ",
    "Practice",
]

ID_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


# ============================================================
# SOURCE TAXONOMY
# Existing taxonomy is preserved exactly during normalization.
# Do not silently rename existing topic/subtopic/microtopic slugs.
# ============================================================

MATH_SYLLABUS = [
    {
        "topic": "Number_System",
        "title_hi": "संख्या पद्धति",
        "subtopics": [
            {
                "name": "Number_Types_and_Place_Value",
                "title_hi": "संख्याओं के प्रकार एवं स्थानीय मान",
                "micros": [
                    "Natural_Whole_Integers_Rational_Reals",
                    "Place_Value_Face_Value_Expanded_Form",
                ],
            },
            {
                "name": "Divisibility_and_Remainders",
                "title_hi": "विभाज्यता एवं शेषफल",
                "micros": [
                    "Divisibility_Rules_and_Remainder_Theorem",
                    "Unit_Digit_and_Trailing_Zeros",
                ],
            },
            {
                "name": "Prime_Factors_and_Factor_Counting",
                "title_hi": "अभाज्य गुणनखंड एवं गुणनखंड गणना",
                "micros": [
                    "Prime_Composite_CoPrime_Properties",
                    "Factor_Counting_and_Sum_of_Factors",
                ],
            },
        ],
    },
    {
        "topic": "Fractions_and_Decimals",
        "title_hi": "भिन्न एवं दशमलव",
        "subtopics": [
            {
                "name": "Types_and_Operations",
                "title_hi": "प्रकार एवं संक्रियाएँ",
                "micros": [
                    "Proper_Improper_Mixed_Comparison",
                    "Fundamental_Operations_on_Fractions",
                ],
            },
            {
                "name": "Decimal_Numbers",
                "title_hi": "दशमलव संख्याएँ",
                "micros": [
                    "Terminating_NonTerminating_Decimals",
                    "Pure_Mixed_Recurring_to_Fractions",
                ],
            },
        ],
    },
    {
        "topic": "HCF_and_LCM",
        "title_hi": "महत्तम समापवर्तक एवं लघुत्तम समापवर्त्य",
        "subtopics": [
            {
                "name": "Methods_of_HCF_LCM",
                "title_hi": "HCF एवं LCM की विधियाँ",
                "micros": [
                    "Factor_and_Division_Methods",
                    "HCF_LCM_of_Fractions_Decimals",
                ],
            },
            {
                "name": "Applications",
                "title_hi": "अनुप्रयोग",
                "micros": [
                    "Product_Formula_LCM_HCF_Relation",
                    "Bells_Circular_Tracks_Equal_Remainder",
                ],
            },
        ],
    },
    {
        "topic": "Simplification_Surds_Indices",
        "title_hi": "सरलीकरण, करणी एवं घातांक",
        "subtopics": [
            {
                "name": "Simplification_and_Roots",
                "title_hi": "सरलीकरण एवं वर्ग/घनमूल",
                "micros": [
                    "VBODMAS_Rule_and_Brackets",
                    "Algebraic_Identity_Simplifications",
                ],
            },
            {
                "name": "Square_and_Cube_Roots",
                "title_hi": "वर्गमूल एवं घनमूल",
                "micros": [
                    "Square_and_Cube_Root_Methods",
                    "Approximation_and_Decimal_Roots",
                ],
            },
            {
                "name": "Indices_and_Surds",
                "title_hi": "घातांक एवं करणी",
                "micros": [
                    "Laws_of_Indices_Unknown_Powers",
                    "Surds_Comparison_and_Rationalization",
                ],
            },
        ],
    },
    {
        "topic": "Percentage",
        "title_hi": "प्रतिशत",
        "subtopics": [
            {
                "name": "Percentage_Basics",
                "title_hi": "प्रतिशत की मूल अवधारणाएँ",
                "micros": [
                    "Fraction_Decimal_Percent_Conversion",
                    "Successive_Percentage_Change",
                ],
            },
            {
                "name": "Applications_of_Percentage",
                "title_hi": "प्रतिशत के अनुप्रयोग",
                "micros": [
                    "Income_Expenditure_Consumption_Price",
                    "Exam_Scores_Election_Population_Problems",
                ],
            },
        ],
    },
    {
        "topic": "Profit_Loss_and_Discount",
        "title_hi": "लाभ, हानि एवं बट्टा",
        "subtopics": [
            {
                "name": "Profit_and_Loss",
                "title_hi": "लाभ एवं हानि",
                "micros": [
                    "Cost_Selling_Price_Margin_Calculations",
                    "Equal_SP_and_Cost_Ratio_Cases",
                ],
            },
            {
                "name": "Discount_and_Marked_Price",
                "title_hi": "बट्टा एवं अंकित मूल्य",
                "micros": [
                    "Marked_Price_and_Successive_Discounts",
                    "Dishonest_Trader_Faulty_Weights",
                ],
            },
        ],
    },
    {
        "topic": "Simple_and_Compound_Interest",
        "title_hi": "साधारण एवं चक्रवृद्धि ब्याज",
        "subtopics": [
            {
                "name": "Simple_Interest",
                "title_hi": "साधारण ब्याज",
                "micros": [
                    "Principal_Rate_Time_Amount_Formulas",
                    "Installment_Problems_Varying_Rates",
                ],
            },
            {
                "name": "Compound_Interest",
                "title_hi": "चक्रवृद्धि ब्याज",
                "micros": [
                    "Annual_HalfYearly_Compounding",
                    "Difference_Between_CI_and_SI",
                ],
            },
        ],
    },
    {
        "topic": "Ratio_Proportion_Unitary_Method",
        "title_hi": "अनुपात, समानुपात एवं एकक विधि",
        "subtopics": [
            {
                "name": "Ratio_and_Proportion",
                "title_hi": "अनुपात एवं समानुपात",
                "micros": [
                    "Simple_Compound_Continued_Ratios",
                    "Mean_Third_Fourth_Proportional_Coins",
                ],
            },
            {
                "name": "Unitary_Method_and_Variation",
                "title_hi": "एकक विधि एवं परिवर्तन",
                "micros": [
                    "Direct_and_Inverse_Variation",
                    "Partnership_Profit_Sharing_Time",
                ],
            },
        ],
    },
    {
        "topic": "Work_Time_Pipes_Cisterns_UPTET",
        "title_hi": "कार्य, समय, नल एवं टंकी",
        "subtopics": [
            {
                "name": "Work_and_Efficiency",
                "title_hi": "कार्य एवं दक्षता",
                "micros": [
                    "Individual_Group_Work_Efficiency",
                    "Alternate_Days_Leaving_Joining_Work",
                ],
            },
            {
                "name": "Pipes_and_Cisterns",
                "title_hi": "नल एवं टंकी",
                "micros": [
                    "Inlet_Outlet_Net_Efficiency",
                    "Leakage_and_Sequential_Opening_Problems",
                ],
            },
        ],
    },
    {
        "topic": "Speed_Time_Distance",
        "title_hi": "चाल, समय एवं दूरी",
        "subtopics": [
            {
                "name": "Speed_Time_Basics",
                "title_hi": "चाल एवं समय की मूल अवधारणाएँ",
                "micros": [
                    "Unit_Conversion_and_Average_Speed",
                    "Relative_Speed_Concepts",
                ],
            },
            {
                "name": "Applications",
                "title_hi": "अनुप्रयोग",
                "micros": [
                    "Train_Passing_Poles_Platforms",
                    "Boats_Upstream_Downstream_Flow",
                ],
            },
        ],
    },
    {
        "topic": "Measurement_Money_Time_CTET",
        "title_hi": "मापन, धन एवं समय",
        "subtopics": [
            {
                "name": "Measurement",
                "title_hi": "मापन",
                "micros": [
                    "Length_Mass_Capacity_Conversions",
                    "NonStandard_to_Standard_Metric_Transition",
                ],
            },
            {
                "name": "Money_and_Time",
                "title_hi": "धन एवं समय",
                "micros": [
                    "Currency_Billing_Transactions",
                    "Time_Intervals_Railway_Schedules_Calendar",
                ],
            },
        ],
    },
    {
        "topic": "Shapes_Spatial_Understanding_Geometry",
        "title_hi": "आकृतियाँ, स्थानिक समझ एवं ज्यामिति",
        "subtopics": [
            {
                "name": "Lines_and_Angles",
                "title_hi": "रेखाएँ एवं कोण",
                "micros": [
                    "Lines_Rays_Angles_Types",
                    "Parallel_Lines_Transversal_Theorems",
                ],
            },
            {
                "name": "Triangles_and_Quadrilaterals",
                "title_hi": "त्रिभुज एवं चतुर्भुज",
                "micros": [
                    "Triangle_Angle_Sum_Congruence_Similarity",
                    "Quadrilateral_Types_Diagonal_Properties",
                ],
            },
            {
                "name": "Circle_Geometry",
                "title_hi": "वृत्त ज्यामिति",
                "micros": [
                    "Radius_Chord_Arc_Sector_Properties",
                    "Central_Inscribed_Angles_Cyclic_Quads",
                ],
            },
        ],
    },
    {
        "topic": "Mensuration_2D",
        "title_hi": "समतलीय क्षेत्रमिति",
        "subtopics": [
            {
                "name": "Triangle_and_Circle_Mensuration",
                "title_hi": "त्रिभुज एवं वृत्त की क्षेत्रमिति",
                "micros": [
                    "Equilateral_Isosceles_Heron_Formula",
                    "Circle_Circumference_Area_Ring",
                ],
            },
            {
                "name": "Quadrilateral_Mensuration",
                "title_hi": "चतुर्भुज की क्षेत्रमिति",
                "micros": [
                    "Rectangle_Square_Diagonals_Pathways",
                    "Parallelogram_Rhombus_Trapezium_Area",
                ],
            },
        ],
    },
    {
        "topic": "Mensuration_3D_UPTET_Paper2",
        "title_hi": "ठोस आकृतियों की क्षेत्रमिति",
        "subtopics": [
            {
                "name": "Cuboid_and_Cube",
                "title_hi": "घनाभ एवं घन",
                "micros": [
                    "Surface_Area_Volume_Diagonal_Formulae",
                    "Four_Walls_Area_Hollow_Boxes",
                ],
            },
            {
                "name": "Cylinder_Cone_Sphere",
                "title_hi": "बेलन, शंकु एवं गोला",
                "micros": [
                    "Right_Circular_Cylinder_Surface_Volume",
                    "Right_Circular_Cone_Slant_Height",
                    "Solid_Hollow_Sphere_Hemisphere",
                ],
            },
        ],
    },
    {
        "topic": "Algebra_UPTET_Paper2",
        "title_hi": "बीजगणित",
        "subtopics": [
            {
                "name": "Expressions_and_Polynomials",
                "title_hi": "व्यंजक एवं बहुपद",
                "micros": [
                    "Variables_Coefficients_Polynomial_Operations",
                    "Standard_Algebraic_Identities_Applications",
                ],
            },
            {
                "name": "Equations_and_Factorization",
                "title_hi": "समीकरण एवं गुणनखंड",
                "micros": [
                    "Linear_Equations_One_Two_Variables",
                    "Polynomial_Factorization_Quadratic_Roots",
                ],
            },
        ],
    },
    {
        "topic": "Statistics_and_Probability",
        "title_hi": "सांख्यिकी एवं प्रायिकता",
        "subtopics": [
            {
                "name": "Statistics",
                "title_hi": "सांख्यिकी",
                "micros": [
                    "Mean_Median_Mode_Ungrouped_Grouped",
                    "Range_and_Empirical_Relationship",
                ],
            },
            {
                "name": "Data_Representation_and_Probability",
                "title_hi": "आँकड़ा निरूपण एवं प्रायिकता",
                "micros": [
                    "Bar_Graph_Histogram_Pie_Chart",
                    "Classical_Probability_Coins_Dice_Cards",
                ],
            },
        ],
    },
    {
        "topic": "Patterns_Symmetry_Nets_CTET",
        "title_hi": "प्रतिरूप, सममिति एवं जाल",
        "subtopics": [
            {
                "name": "Symmetry_and_Patterns",
                "title_hi": "सममिति एवं प्रतिरूप",
                "micros": [
                    "Line_Symmetry_Axes_Counting",
                    "Rotational_Symmetry_Order_Angle",
                ],
            },
            {
                "name": "Patterns_and_Nets",
                "title_hi": "प्रतिरूप एवं ठोस आकृतियों के जाल",
                "micros": [
                    "Number_Shape_Patterns_Generalization",
                    "TwoD_Nets_of_3D_Solids_Tessellation",
                ],
            },
        ],
    },
    {
        "topic": "Nature_of_Mathematics_Logical_Thinking_CTET",
        "title_hi": "गणित की प्रकृति एवं तार्किक चिंतन",
        "subtopics": [
            {
                "name": "Nature_and_Reasoning",
                "title_hi": "गणित की प्रकृति एवं तर्क",
                "micros": [
                    "Abstract_Hierarchical_Logical_Nature",
                    "Inductive_vs_Deductive_Reasoning",
                ],
            },
            {
                "name": "Mathematical_Language",
                "title_hi": "गणितीय भाषा एवं संकल्पनाएँ",
                "micros": [
                    "Mathematical_Symbols_Terms_Definitions",
                    "Axioms_Postulates_Conjectures_Theorems",
                ],
            },
        ],
    },
    {
        "topic": "Curriculum_Place_and_Objectives",
        "title_hi": "गणित पाठ्यचर्या, स्थान एवं उद्देश्य",
        "subtopics": [
            {
                "name": "Aims_and_Objectives",
                "title_hi": "उद्देश्य एवं गणितीकरण",
                "micros": [
                    "Narrow_vs_Higher_Aims_Mathematization",
                    "Revised_Bloom_Taxonomy_in_Math",
                ],
            },
            {
                "name": "Curriculum_Frameworks",
                "title_hi": "पाठ्यचर्या एवं नीतिगत दृष्टिकोण",
                "micros": [
                    "NCF_2005_Vision_for_Mathematics",
                    "NEP_2020_Computational_Mathematical_Thinking",
                ],
            },
        ],
    },
    {
        "topic": "Teaching_Methods_and_Van_Hiele_Model",
        "title_hi": "गणित शिक्षण विधियाँ एवं वान हिले मॉडल",
        "subtopics": [
            {
                "name": "Teaching_Methods",
                "title_hi": "शिक्षण विधियाँ",
                "micros": [
                    "Inductive_Deductive_Analytic_Synthetic",
                    "Problem_Solving_Heuristic_Project_Method",
                ],
            },
            {
                "name": "Van_Hiele_Model",
                "title_hi": "वान हिले मॉडल",
                "micros": [
                    "Level_0_Visualization_and_Level_1_Analysis",
                    "Level_2_Informal_Level_3_Deduction_Rigor",
                ],
            },
        ],
    },
    {
        "topic": "Math_Manipulatives_TLM_ICT_CTET",
        "title_hi": "गणितीय उपकरण, TLM एवं ICT",
        "subtopics": [
            {
                "name": "Manipulatives_and_TLM",
                "title_hi": "गणितीय उपकरण एवं शिक्षण सामग्री",
                "micros": [
                    "Geoboard_for_Shapes_Perimeter_Area",
                    "Abacus_Place_Value_Visually_Impaired",
                    "Tangram_and_Dienes_Base_10_Blocks",
                    "Grid_Paper_Dot_Paper_Decimals_Symmetry",
                ],
            },
            {
                "name": "ICT_and_Math_Lab",
                "title_hi": "ICT एवं गणित प्रयोगशाला",
                "micros": [
                    "Math_Lab_Activities_Low_Cost_TLM",
                    "GeoGebra_DIKSHA_Simulations",
                ],
            },
        ],
    },
    {
        "topic": "Error_Analysis_Alternative_Conceptions",
        "title_hi": "त्रुटि विश्लेषण एवं वैकल्पिक अवधारणाएँ",
        "subtopics": [
            {
                "name": "Mathematical_Errors",
                "title_hi": "गणितीय त्रुटियाँ",
                "micros": [
                    "Procedural_vs_Conceptual_Errors",
                    "Careless_Errors_and_Language_Barriers",
                ],
            },
            {
                "name": "Alternative_Conceptions",
                "title_hi": "वैकल्पिक अवधारणाएँ",
                "micros": [
                    "Child_Math_Thinking_Naive_Theories",
                    "Error_Guided_Remedial_Design",
                ],
            },
        ],
    },
    {
        "topic": "Assessment_Evaluation_Remedial_Teaching",
        "title_hi": "आकलन, मूल्यांकन एवं उपचारात्मक शिक्षण",
        "subtopics": [
            {
                "name": "Assessment_and_Evaluation",
                "title_hi": "आकलन एवं मूल्यांकन",
                "micros": [
                    "Formative_Summative_Math_Assessment",
                    "Math_Rubrics_Portfolios_Open_Ended_Tasks",
                ],
            },
            {
                "name": "Diagnostic_and_Remedial",
                "title_hi": "नैदानिक एवं उपचारात्मक शिक्षण",
                "micros": [
                    "Diagnostic_Testing_Gap_Identification",
                    "Remedial_Lesson_Planning_Individualized",
                ],
            },
        ],
    },
    {
        "topic": "FLN_and_National_Math_Missions",
        "title_hi": "FLN एवं राष्ट्रीय गणितीय पहल",
        "subtopics": [
            {
                "name": "Foundational_Numeracy",
                "title_hi": "आधारभूत संख्यात्मकता",
                "micros": [
                    "Foundational_Numeracy_Milestones",
                    "Pre_Number_Concepts_Operations_Grades_1_3",
                ],
            },
            {
                "name": "Activity_Based_Math_and_Anxiety",
                "title_hi": "गतिविधि आधारित गणित एवं गणितीय चिंता",
                "micros": [
                    "Toy_and_Activity_Based_Math_Pedagogy",
                    "Overcoming_Math_Anxiety_and_Phobia",
                ],
            },
        ],
    },
]


# ============================================================
# VALIDATION
# ============================================================

def fail(message):
    raise ValueError(f"VALIDATION ERROR: {message}")


def validate_id(value, label):
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty string.")

    if not ID_PATTERN.fullmatch(value):
        fail(
            f"{label} has invalid ID '{value}'. "
            "Allowed characters: A-Z, 0-9, underscore."
        )


def validate_taxonomy():
    if not isinstance(MATH_SYLLABUS, list) or not MATH_SYLLABUS:
        fail("MATH_SYLLABUS must be a non-empty list.")

    topic_ids = set()
    subtopic_ids = set()
    micro_ids = set()

    for topic_index, topic in enumerate(MATH_SYLLABUS, start=1):
        topic_slug = topic.get("topic")

        if not topic_slug:
            fail(f"Topic {topic_index} has no topic slug.")

        validate_id(f"T{topic_index:02d}_{topic_slug}", f"Topic {topic_index}")

        topic_id = f"T{topic_index:02d}_{topic_slug}"

        if topic_id in topic_ids:
            fail(f"Duplicate topic ID: {topic_id}")

        topic_ids.add(topic_id)

        subtopics = topic.get("subtopics")

        if not isinstance(subtopics, list) or not subtopics:
            fail(f"{topic_id} has no subtopics.")

        for sub_index, subtopic in enumerate(subtopics, start=1):
            sub_slug = subtopic.get("name")

            if not sub_slug:
                fail(f"{topic_id} subtopic {sub_index} has no slug.")

            sub_id = f"{topic_id}_ST{sub_index:02d}_{sub_slug}"
            validate_id(sub_id, f"Subtopic {topic_id}/{sub_index}")

            if sub_id in subtopic_ids:
                fail(f"Duplicate subtopic ID: {sub_id}")

            subtopic_ids.add(sub_id)

            micros = subtopic.get("micros")

            if not isinstance(micros, list) or not micros:
                fail(f"{sub_id} has no microtopics.")

            for micro_index, micro_slug in enumerate(micros, start=1):
                if not isinstance(micro_slug, str) or not micro_slug:
                    fail(f"{sub_id} microtopic {micro_index} is invalid.")

                micro_id = f"{sub_id}_M{micro_index:02d}_{micro_slug}"
                validate_id(
                    micro_id,
                    f"MicroTopic {topic_id}/{sub_index}/{micro_index}",
                )

                if micro_id in micro_ids:
                    fail(f"Duplicate microtopic ID: {micro_id}")

                micro_ids.add(micro_id)

    return len(topic_ids), len(subtopic_ids), len(micro_ids)


# ============================================================
# FILE HELPERS
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_name(path.name + ".tmp")

    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(
            data,
            handle,
            ensure_ascii=False,
            indent=2,
        )
        handle.write("\n")

    os.replace(temporary, path)


def write_text_if_missing(path, content):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)


def write_json_if_missing(path, data):
    if not path.exists():
        write_json_atomic(path, data)


# ============================================================
# ASSET SCAFFOLD
# ============================================================

def ensure_leaf_assets(micro_path, micro_id, micro_slug):
    created_files = 0
    created_directories = 0

    for asset in LEAF_ASSETS:
        asset_path = micro_path / asset

        if not asset_path.exists():
            asset_path.mkdir(parents=True, exist_ok=True)
            created_directories += 1

        if asset in {"Concept", "Short_Notes", "Practice"}:
            content_path = asset_path / "content.md"

            if not content_path.exists():
                write_text_if_missing(
                    content_path,
                    (
                        f"# {micro_slug}\n\n"
                        f"Asset: {asset}\n"
                        f"MicroTopic ID: {micro_id}\n\n"
                        "विषयवस्तु संकलन प्रगति पर है।\n"
                    ),
                )
                created_files += 1

        elif asset in {"PYQ", "MCQ"}:
            content_path = asset_path / "content.json"

            if not content_path.exists():
                write_json_if_missing(
                    content_path,
                    {
                        "microtopic_id": micro_id,
                        "asset_type": asset,
                        "status": "scaffolded",
                        "items": [],
                    },
                )
                created_files += 1

    return created_directories, created_files


# ============================================================
# MANIFEST BUILDER
# ============================================================

def build_manifest():
    topics = []

    total_subtopics = 0
    total_microtopics = 0

    created_directories = 0
    created_files = 0

    for topic_index, topic in enumerate(MATH_SYLLABUS, start=1):
        topic_id = f"T{topic_index:02d}_{topic['topic']}"

        topic_path = BASE_PATH / (
            f"Topic_{topic_index:02d}_{topic['topic']}"
        )

        if not topic_path.exists():
            topic_path.mkdir(parents=True, exist_ok=True)
            created_directories += 1

        subtopic_entries = []

        for sub_index, subtopic in enumerate(
            topic["subtopics"],
            start=1,
        ):
            subtopic_id = (
                f"{topic_id}_ST{sub_index:02d}_{subtopic['name']}"
            )

            subtopic_path = topic_path / (
                f"Subtopic_{sub_index:02d}_{subtopic['name']}"
            )

            if not subtopic_path.exists():
                subtopic_path.mkdir(parents=True, exist_ok=True)
                created_directories += 1

            micro_entries = []

            for micro_index, micro_slug in enumerate(
                subtopic["micros"],
                start=1,
            ):
                micro_id = (
                    f"{subtopic_id}_M{micro_index:02d}_{micro_slug}"
                )

                micro_path = subtopic_path / (
                    f"MicroTopic_{micro_index:02d}_{micro_slug}"
                )

                if not micro_path.exists():
                    micro_path.mkdir(parents=True, exist_ok=True)
                    created_directories += 1

                new_dirs, new_files = ensure_leaf_assets(
                    micro_path,
                    micro_id,
                    micro_slug,
                )

                created_directories += new_dirs
                created_files += new_files

                micro_entries.append(
                    {
                        "id": micro_id,
                        "slug": micro_slug,
                        "order": micro_index,
                        "assets": LEAF_ASSETS,
                    }
                )

            total_microtopics += len(micro_entries)
            total_subtopics += 1

            subtopic_entries.append(
                {
                    "id": subtopic_id,
                    "slug": subtopic["name"],
                    "title_hi": subtopic.get(
                        "title_hi",
                        subtopic["name"],
                    ),
                    "order": sub_index,
                    "micro_topics": micro_entries,
                }
            )

        topics.append(
            {
                "id": topic_id,
                "slug": topic["topic"],
                "title_hi": topic.get(
                    "title_hi",
                    topic["topic"],
                ),
                "order": topic_index,
                "subtopics": subtopic_entries,
            }
        )

    manifest = {
        "schema_version": "0.1.0",
        "framework_version": FRAMEWORK_VERSION,
        "content_version": CONTENT_VERSION,
        "taxonomy_version": TAXONOMY_VERSION,
        "status": STATUS,
        "exam_scope": EXAM_SCOPE,
        "paper_scope": PAPER_SCOPE,
        "subject": {
            "id": SUBJECT_ID,
            "type": SUBJECT_TYPE,
            "name_en": SUBJECT_NAME_EN,
            "name_hi": SUBJECT_NAME_HI,
        },
        "total_topics": len(topics),
        "total_subtopics": total_subtopics,
        "total_microtopics": total_microtopics,
        "asset_types": LEAF_ASSETS,
        "topics": topics,
    }

    return (
        manifest,
        created_directories,
        created_files,
    )


# ============================================================
# MASTER MANIFEST RECONCILIATION
# ============================================================

def reconcile_master_manifest():
    if not MASTER_MANIFEST.exists():
        fail(
            f"Master manifest does not exist: "
            f"{MASTER_MANIFEST}"
        )

    master = load_json(MASTER_MANIFEST)

    subjects = master.setdefault("subjects", [])

    matching = [
        subject
        for subject in subjects
        if subject.get("id") == SUBJECT_ID
    ]

    if len(matching) > 1:
        fail(
            f"Duplicate {SUBJECT_ID} entries found in master manifest."
        )

    entry = matching[0] if matching else {}

    entry.update(
        {
            "id": SUBJECT_ID,
            "name_en": SUBJECT_NAME_EN,
            "name_hi": SUBJECT_NAME_HI,
            "directory": "Mathematics",
            "manifest_path": "Mathematics/manifest.json",
            "status": STATUS,
            "total_topics": len(MATH_SYLLABUS),
            "framework_version": FRAMEWORK_VERSION,
            "taxonomy_version": TAXONOMY_VERSION,
        }
    )

    if not matching:
        subjects.append(entry)

    # During the framework-audit phase, this field represents
    # subjects participating in the framework, not only published
    # subjects. Preserve existing architecture.
    master["active_subjects_count"] = len(subjects)

    if "total_planned_subjects" not in master:
        master["total_planned_subjects"] = len(subjects)

    write_json_atomic(MASTER_MANIFEST, master)

    return master


# ============================================================
# FINAL VERIFICATION
# ============================================================

def final_verify(manifest):
    if not SUBJECT_MANIFEST.exists():
        fail("Subject manifest was not created.")

    stored = load_json(SUBJECT_MANIFEST)

    if stored.get("subject", {}).get("id") != SUBJECT_ID:
        fail("Subject manifest has incorrect subject ID.")

    if stored.get("status") != STATUS:
        fail("Subject manifest has incorrect lifecycle status.")

    if stored.get("total_topics") != len(MATH_SYLLABUS):
        fail("Subject manifest topic count mismatch.")

    if len(stored.get("topics", [])) != len(MATH_SYLLABUS):
        fail("Subject manifest topic entry count mismatch.")

    master = load_json(MASTER_MANIFEST)

    matches = [
        x for x in master.get("subjects", [])
        if x.get("id") == SUBJECT_ID
    ]

    if len(matches) != 1:
        fail("Master manifest must contain exactly one MATH entry.")

    master_entry = matches[0]

    if master_entry.get("status") != STATUS:
        fail("Master MATH status mismatch.")

    if master_entry.get("manifest_path") != (
        "Mathematics/manifest.json"
    ):
        fail("Master MATH manifest path mismatch.")

    return stored


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("SISKILL — MATH FRAMEWORK GENERATOR")
    print("=" * 60)

    print(f"Subject ID       : {SUBJECT_ID}")
    print(f"Subject          : {SUBJECT_NAME_EN}")
    print(f"Framework        : {FRAMEWORK_VERSION}")
    print(f"Taxonomy         : {TAXONOMY_VERSION}")
    print(f"Status           : {STATUS}")
    print()

    print("1. Validating Math taxonomy...")

    topic_count, subtopic_count, microtopic_count = (
        validate_taxonomy()
    )

    print(
        f"   OK — {topic_count} topics, "
        f"{subtopic_count} subtopics, "
        f"{microtopic_count} microtopics validated."
    )

    print("2. Reconciling Math directory scaffold...")

    (
        manifest,
        new_directories,
        new_files,
    ) = build_manifest()

    print("   OK — existing scaffold preserved.")
    print(f"   New directories : {new_directories}")
    print(f"   New files       : {new_files}")

    print("3. Writing Math subject manifest...")

    write_json_atomic(
        SUBJECT_MANIFEST,
        manifest,
    )

    print(f"   OK — {SUBJECT_MANIFEST}")

    print("4. Reconciling master manifest...")

    reconcile_master_manifest()

    print("   Existing MATH entry reconciled.")

    print("5. Running final verification...")

    verified = final_verify(manifest)

    print()
    print("=" * 60)
    print("MATH FRAMEWORK GENERATION COMPLETE")
    print("=" * 60)

    print(f"Topics       : {verified['total_topics']}")
    print(f"Subtopics    : {verified['total_subtopics']}")
    print(f"MicroTopics  : {verified['total_microtopics']}")
    print(f"Asset Types  : {len(verified['asset_types'])}")
    print(f"Status       : {verified['status']}")

    print()
    print("Subject manifest:")
    print(f"  {SUBJECT_MANIFEST}")

    print()
    print("Master manifest:")
    print(f"  {MASTER_MANIFEST}")

    print()
    print("Existing directories/files were not deleted.")
    print("=" * 60)


if __name__ == "__main__":
    main()

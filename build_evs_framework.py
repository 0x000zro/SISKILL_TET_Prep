#!/usr/bin/env python3
"""
SISKILL — EVS Framework Generator

Purpose:
    Generate and reconcile the Environmental Studies framework
    without destructive recreation of the existing scaffold.

Lifecycle:
    planned -> scaffolded -> content_generated -> validating
    -> review -> verified -> published -> archived

This generator preserves the existing EVS taxonomy:
    24 Topics
    52 Subtopics
    115 MicroTopics

It does NOT delete or rename existing production content.
"""

import json
import os
import re
import tempfile
from pathlib import Path


BASE_PATH = "UPTET_CTET/Paper_1_and_2/Environmental_Studies"
MASTER_MANIFEST = "UPTET_CTET/Paper_1_and_2/master_manifest.json"

FRAMEWORK_VERSION = "1.0.0"
CONTENT_VERSION = "0.1.0"
TAXONOMY_VERSION = "1.0.0"

SUBJECT_ID = "EVS"
SUBJECT_TYPE = "environmental_studies_pedagogy"

SUBJECT_NAME_EN = "Environmental Studies and Pedagogy"
SUBJECT_NAME_HI = "पर्यावरण अध्ययन एवं शिक्षण शास्त्र"

EXAM_SCOPE = ["UPTET", "CTET"]
PAPER_SCOPE = ["Paper_1", "Paper_2"]

STATUS = "scaffolded"

LEAF_ASSETS = [
    "Concept",
    "Short_Notes",
    "PYQ",
    "MCQ",
    "Practice",
]

ASSET_LAYOUT = {
    "Concept": "content.md",
    "Short_Notes": "content.md",
    "PYQ": "content.json",
    "MCQ": "content.json",
    "Practice": "content.md",
}

ID_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


# ---------------------------------------------------------------------------
# PRESERVED EVS TAXONOMY
# ---------------------------------------------------------------------------

EVS_SYLLABUS = [{'id': 'T01',
  'topic': 'Family_and_Friends_Relations_Work_Play',
  'title': 'परिवार एवं मित्र — संबंध, कार्य एवं खेल',
  'subtopics': [{'id': 'ST01_01',
                 'name': 'Family_Structure_Social_Aspects',
                 'micros': ['Nuclear_Joint_Family_Dynamics',
                            'Family_Relations_Child_Marriage_Abolition']},
                {'id': 'ST01_02',
                 'name': 'Work_Play_Child_Labor',
                 'micros': ['Traditional_Games_Child_Development',
                            'Work_Occupations_Child_Labor_Laws']}]},
 {'id': 'T02',
  'topic': 'Animals_Fauna_and_Adaptations',
  'title': 'जंतु एवं प्राणी जगत',
  'subtopics': [{'id': 'ST02_01',
                 'name': 'Mammals_Birds_Reptiles_CTET',
                 'micros': ['Animal_Traits_Sloth_Tiger_Elephant_Snakes',
                            'Bird_Characteristics_Beaks_Nests_Vision']},
                {'id': 'ST02_02',
                 'name': 'Insects_and_Microorganisms',
                 'micros': ['Social_Insects_Honeybees_Ants_Termites',
                            'Silkworm_Earthworm_Sensory_Adaptations']}]},
 {'id': 'T03',
  'topic': 'Plants_Flora_Natural_Vegetation',
  'title': 'पादप एवं वनस्पति जगत',
  'subtopics': [{'id': 'ST03_01',
                 'name': 'Plant_Anatomy_Special_Plants_CTET',
                 'micros': ['Roots_Stems_Leaves_Photosynthesis_Transpiration',
                            'Insectivorous_Nepenthes_Desert_Oak_Banyan']},
                {'id': 'ST03_02',
                 'name': 'Seeds_Dispersal_Agriculture',
                 'micros': ['Seed_Germination_Dispersal_Foreign_Seeds',
                            'Cropping_Patterns_Jhum_Organic_Farming']}]},
 {'id': 'T04',
  'topic': 'Food_Nutrition_Cooking_Diseases',
  'title': 'भोजन, पोषण एवं स्वास्थ्य',
  'subtopics': [{'id': 'ST04_01',
                 'name': 'Nutrition_and_Preservation_CTET',
                 'micros': ['Nutrients_Deficiency_Diseases_Vitamins',
                            'Food_Preservation_Techniques_Mamidi_Tandra',
                            'Regional_Cuisines_Ling_hu_fen_Tapioca_Fish']},
                {'id': 'ST04_02',
                 'name': 'Digestion_and_Infectious_Diseases',
                 'micros': ['Human_Digestion_Dr_Beaumont_Experiments',
                            'Water_Mosquito_Borne_Diseases_Malaria_Ross']}]},
 {'id': 'T05',
  'topic': 'Shelter_Regional_Habitats_Architecture_CTET',
  'title': 'आश्रय, बस्तियां एवं आवास विविधता',
  'subtopics': [{'id': 'ST05_01',
                 'name': 'Geographical_Shelter_Diversity',
                 'micros': ['Ladakh_Stone_Houses_Changpa_Rebo_Tents',
                            'Assam_Bamboo_Stilt_Manali_Houses',
                            'Rajasthan_Mud_Houses_Kashmir_Houseboats']},
                {'id': 'ST05_02',
                 'name': 'Shelter_Types_Sanitation_Waste',
                 'micros': ['Temporary_Permanent_Public_Housing',
                            'Sanitation_Waste_Management_Uninvited_Pests']}]},
 {'id': 'T06',
  'topic': 'Water_Resources_Cycles_Conservation',
  'title': 'जल संसाधन, जल चक्र एवं संरक्षण',
  'subtopics': [{'id': 'ST06_01',
                 'name': 'Water_Sources_Historic_Management_CTET',
                 'micros': ['Water_Sources_Groundwater_Depletion_Pollution',
                            'Traditional_Stepwells_Bawri_Ghadsisar_AlBiruni']},
                {'id': 'ST06_02',
                 'name': 'Properties_and_Movements',
                 'micros': ['Water_Properties_Dead_Sea_Density_Buoyancy',
                            'Water_Movements_Tarun_Bharat_Bhima_Sangh']}]},
 {'id': 'T07',
  'topic': 'Travel_Transport_Mapping_Space_CTET',
  'title': 'यात्रा, परिवहन, मानचित्रण एवं अंतरिक्ष',
  'subtopics': [{'id': 'ST07_01',
                 'name': 'Mapping_Direction_Scale_Skills',
                 'micros': ['Indian_Map_States_Coastal_Relative_Position',
                            'Direction_Distance_Problems_Train_Timetables']},
                {'id': 'ST07_02',
                 'name': 'Mountaineering_Space_Transport',
                 'micros': ['Bachendri_Pal_Mount_Everest_Expedition',
                            'Sunita_Williams_Kalpana_Chawla_Space',
                            'Local_Transport_Vallam_Ferry_Jugaad_Tickets']}]},
 {'id': 'T08',
  'topic': 'Things_We_Make_and_Do_Crafts_Heritage',
  'title': 'वस्तुएं जो हम बनाते और करते हैं',
  'subtopics': [{'id': 'ST08_01',
                 'name': 'Traditional_Arts_and_Textiles_CTET',
                 'micros': ['Folk_Paintings_Madhubani_Warli_Pattachitra',
                            'Textiles_Pochampally_Pashmina_Chikankari']},
                {'id': 'ST08_02',
                 'name': 'Metals_Minerals_Pottery_Tools',
                 'micros': ['Bronze_Alloy_Copper_Tin_Pottery_Making',
                            'Traditional_Occupations_Agricultural_Tools']}]},
 {'id': 'T09',
  'topic': 'Ecology_Ecosystems_Biomes_UPTET',
  'title': 'पर्यावरण एवं पारिस्थितिकी तंत्र',
  'subtopics': [{'id': 'ST09_01',
                 'name': 'Ecosystem_Structure',
                 'micros': ['Ecology_Haaeckel_Ecosystem_Tansley_Concepts',
                            'Biotic_Abiotic_Producers_Consumers_Decomposers']},
                {'id': 'ST09_02',
                 'name': 'Food_Chains_and_Pyramids',
                 'micros': ['Food_Chains_Webs_Lindeman_Ten_Percent_Law',
                            'Ecological_Pyramids_Energy_Biomass_Numbers']},
                {'id': 'ST09_03',
                 'name': 'Global_Biomes_and_Aquatic_Systems',
                 'micros': ['Terrestrial_Biomes_Tundra_Taiga_Grasslands',
                            'Aquatic_Coral_Reefs_Mangrove_Ecosystems']}]},
 {'id': 'T10',
  'topic': 'Biodiversity_and_Wildlife_Conservation_UPTET',
  'title': 'जैव विविधता एवं वन्यजीव संरक्षण',
  'subtopics': [{'id': 'ST10_01',
                 'name': 'Biodiversity_Concepts_Hotspots',
                 'micros': ['Biodiversity_Rosen_Alpha_Beta_Gamma_Diversity',
                            'Hotspots_Western_Ghats_Eastern_Himalayas']},
                {'id': 'ST10_02',
                 'name': 'IUCN_Red_List_Conservation_Modes',
                 'micros': ['IUCN_Red_Data_Book_Endangered_Categories',
                            'Insitu_vs_Exsitu_Conservation_Sanctuaries']},
                {'id': 'ST10_03',
                 'name': 'Flagship_Projects_and_Institutes',
                 'micros': ['Project_Tiger_Elephant_Rhino_Crocodile',
                            'Major_National_Parks_Jim_Corbett_Kaziranga',
                            'Wildlife_Institute_of_India_FRI_NGT']}]},
 {'id': 'T11',
  'topic': 'Pollution_Global_Warming_Ozone_Depletion',
  'title': 'पर्यावरण प्रदूषण, वैश्विक तापन एवं ओजोन क्षरण',
  'subtopics': [{'id': 'ST11_01',
                 'name': 'Air_Water_Soil_Noise_Pollution',
                 'micros': ['Air_Pollutants_PM25_Smog_Acid_Rain_Gases',
                            'Water_Pollution_BOD_COD_Eutrophication_Diseases',
                            'Noise_Decibel_Standards_Soil_Degradation']},
                {'id': 'ST11_02',
                 'name': 'Greenhouse_Ozone_Depletion',
                 'micros': ['Greenhouse_Gases_Global_Warming_Dynamics',
                            'Ozone_Depletion_Dobson_Montreal_Protocol']}]},
 {'id': 'T12',
  'topic': 'Environmental_Movements_Laws_Treaties',
  'title': 'पर्यावरण संरक्षण आंदोलन, कानून एवं अंतरराष्ट्रीय सम्मेलन',
  'subtopics': [{'id': 'ST12_01',
                 'name': 'Indian_Environmental_Movements_UPTET',
                 'micros': ['Chipko_Movement_Bahuguna_Gaura_Devi',
                            'Bishnoi_Appiko_Narmada_Bachao_Andolan']},
                {'id': 'ST12_02',
                 'name': 'Environmental_Legislations_India',
                 'micros': ['Wildlife_Protection_Act_1972_Forest_1980',
                            'Environment_Protection_Act_1986_Umbrella_Act']},
                {'id': 'ST12_03',
                 'name': 'Global_Conferences_Protocols',
                 'micros': ['Stockholm_1972_Earth_Summit_1992_Agenda21',
                            'Kyoto_Protocol_Carbon_Credits_Paris_Agreement']}]},
 {'id': 'T13',
  'topic': 'Solar_System_and_Earth_Dynamics_UPTET',
  'title': 'सौरमंडल, पृथ्वी की गतियां एवं खगोलिकी',
  'subtopics': [{'id': 'ST13_01',
                 'name': 'Solar_System_Planets',
                 'micros': ['Sun_Eight_Planets_Classification_Traits',
                            'Satellites_Asteroids_Meteors_Comets']},
                {'id': 'ST13_02',
                 'name': 'Earth_Motions_Coordinates_Eclipses',
                 'micros': ['Rotation_Revolution_Seasons_Perihelion_Aphelion',
                            'Latitudes_Longitudes_IDL_GMT_IST_Calculations',
                            'Tropics_Equator_Solar_Lunar_Eclipses']}]},
 {'id': 'T14',
  'topic': 'Physical_Geography_of_India_UPTET',
  'title': 'भारत का भौतिक भूगोल — पर्वत, पठार, नदियां एवं झीलें',
  'subtopics': [{'id': 'ST14_01',
                 'name': 'Physiography_Mountains_Plateaus',
                 'micros': ['Himalayan_Ranges_Passes_Major_Peaks',
                            'Peninsular_Plateau_Western_Eastern_Ghats_Coasts']},
                {'id': 'ST14_02',
                 'name': 'Drainage_Systems_and_Lakes',
                 'micros': ['Himalayan_Rivers_Ganga_Yamuna_Brahmaputra',
                            'Peninsular_Rivers_Arabian_Sea_Bay_of_Bengal',
                            'Major_Lakes_Wular_Chilika_Sambhar_Waterfalls']}]},
 {'id': 'T15',
  'topic': 'Climate_Soils_Agriculture_Minerals_UPTET',
  'title': 'भारत की जलवायु, मृदा, कृषि एवं खनिज',
  'subtopics': [{'id': 'ST15_01',
                 'name': 'Monsoon_Climate_Soils',
                 'micros': ['Southwest_Northeast_Monsoon_Rainfall',
                            'ICAR_Soil_Classification_Alluvial_Black_Laterite']},
                {'id': 'ST15_02',
                 'name': 'Agriculture_and_Minerals',
                 'micros': ['Crops_Green_Revolution_Swaminathan_White_Rev',
                            'Conventional_Renewable_Energy_Mineral_Belts']}]},
 {'id': 'T16',
  'topic': 'Uttar_Pradesh_Comprehensive_EVS_UPTET',
  'title': 'उत्तर प्रदेश — भूगोल, संस्कृति, मेले, नदियां एवं अभयारण्य',
  'subtopics': [{'id': 'ST16_01',
                 'name': 'UP_Physiography_Drainage',
                 'micros': ['Boundaries_Bhabhar_Terai_Bundelkhand_Plateau',
                            'UP_Rivers_Ganga_Yamuna_Gomti_Saryu_Canals']},
                {'id': 'ST16_02',
                 'name': 'UP_Wildlife_Sanctuaries',
                 'micros': ['Dudhwa_National_Park_Chandraprabha_Katarniaghat',
                            'Bird_Sanctuaries_Nawabganj_LakhBahosi_Bakhira']},
                {'id': 'ST16_03',
                 'name': 'UP_Culture_Fairs_Tribes',
                 'micros': ['Kumbh_Nauchandi_Bateshwar_DewaSharif_Fairs',
                            'Folk_Dances_Charkula_Nautanki_Kajri_Alha',
                            'UP_Tribes_Tharu_Diwali_Mourning_Buksa']}]},
 {'id': 'T17',
  'topic': 'Constitution_Preamble_Citizenship_UPTET',
  'title': 'भारतीय संविधान — ऐतिहासिक विकास, प्रस्तावना एवं नागरिकता',
  'subtopics': [{'id': 'ST17_01',
                 'name': 'Constituent_Assembly_Making',
                 'micros': ['Cabinet_Mission_Drafting_Committee_Ambedkar',
                            'Constitutional_Sources_Borrowed_Features']},
                {'id': 'ST17_02',
                 'name': 'Preamble_and_Citizenship',
                 'micros': ['Preamble_Core_Philosophy_42nd_Amendment',
                            'Citizenship_Provisions_Articles_5_to_11']}]},
 {'id': 'T18',
  'topic': 'Fundamental_Rights_Duties_DPSP_UPTET',
  'title': 'मौलिक अधिकार, मूल कर्तव्य एवं नीति निदेशक तत्व',
  'subtopics': [{'id': 'ST18_01',
                 'name': 'Fundamental_Rights_Part3',
                 'micros': ['Six_Fundamental_Rights_Articles_14_to_30',
                            'Article_32_Writs_Article_21A_RTE_Amendment']},
                {'id': 'ST18_02',
                 'name': 'DPSP_and_Duties',
                 'micros': ['DPSP_Panchayats_Art40_UCC_Art44_Environment_48A',
                            'Fundamental_Duties_Swaran_Singh_Art51A_g']}]},
 {'id': 'T19',
  'topic': 'Governance_and_Local_Self_Govt_UPTET',
  'title': 'शासन प्रणाली — कार्यपालिका, विधायिका, न्यायपालिका एवं स्थानीय स्वशासन',
  'subtopics': [{'id': 'ST19_01',
                 'name': 'Union_Governance_Judiciary',
                 'micros': ['President_Powers_Emergency_Articles_352_356_360',
                            'Parliament_Lok_Sabha_Rajya_Sabha_Prime_Minister',
                            'Supreme_Court_Jurisdiction_Public_Interest_Litigation']},
                {'id': 'ST19_02',
                 'name': 'State_Govt_Panchayati_Raj',
                 'micros': ['Governor_Chief_Minister_State_Legislature',
                            '73rd_Amendment_11th_Schedule_Balwant_Rai_Mehta',
                            '74th_Amendment_12th_Schedule_Municipalities']}]},
 {'id': 'T20',
  'topic': 'Concept_Scope_Integrated_Nature_CTET',
  'title': 'पर्यावरण अध्ययन की संकल्पना, प्रकृति एवं एकीकृत उपागम',
  'subtopics': [{'id': 'ST20_01',
                 'name': 'Integrated_EVS_Concept',
                 'micros': ['EVS_Concept_Scope_Grades_3_to_5',
                            'Integration_of_Science_Social_Science_Environment',
                            'No_Textbook_in_Grades_1_2_Contextual_Teaching']},
                {'id': 'ST20_02',
                 'name': 'Thematic_vs_Topic_Approach',
                 'micros': ['Six_Core_NCERT_Themes_Rationale',
                            'Connecting_Immediate_Environment_to_Global']}]},
 {'id': 'T21',
  'topic': 'Learning_Principles_Science_Social_Interrelation_CTET',
  'title': 'EVS अधिगम के सिद्धांत एवं विज्ञान/सामाजिक विज्ञान से अंतर्संबंध',
  'subtopics': [{'id': 'ST21_01',
                 'name': 'Child_Centered_Principles',
                 'micros': ['Concrete_to_Abstract_Known_to_Unknown',
                            'Local_to_Global_Learning_by_Doing']},
                {'id': 'ST21_02',
                 'name': 'Interdisciplinary_Linkages',
                 'micros': ['Correlation_with_Science_Social_Science',
                            'Multidisciplinary_Holistic_Understanding']}]},
 {'id': 'T22',
  'topic': 'Pedagogical_Methods_Activities_Inquiry_CTET',
  'title': 'शिक्षण विधियां, क्रियाकलाप, प्रयोग एवं अन्वेषण',
  'subtopics': [{'id': 'ST22_01',
                 'name': 'Inquiry_Project_Discussions',
                 'micros': ['Inquiry_Discovery_Problem_Solving_Projects',
                            'Classroom_Discussions_Collaborative_Learning']},
                {'id': 'ST22_02',
                 'name': 'Experiments_and_Field_Trips',
                 'micros': ['Simple_Experiments_Observation_Classification',
                            'Field_Trips_Educational_Excursions_Planning']}]},
 {'id': 'T23',
  'topic': 'TLM_Textbooks_and_ICT_in_EVS_CTET',
  'title': 'शिक्षण अधिगम सामग्री, पाठ्यपुस्तकें एवं आईसीटी',
  'subtopics': [{'id': 'ST23_01',
                 'name': 'NCERT_Textbook_Philosophy',
                 'micros': ['Child_Centered_Narratives_Debiasing_Gender_Caste',
                            'Avoiding_Definitions_Rote_Encouraging_Critique']},
                {'id': 'ST23_02',
                 'name': 'TLM_and_Digital_Integration',
                 'micros': ['Local_No_Cost_TLM_Real_Objects_Models_Globe',
                            'Audio_Visual_Aids_DIKSHA_Simulations']}]},
 {'id': 'T24',
  'topic': 'Assessment_Evaluation_Diagnostics_in_EVS_CTET',
  'title': 'सतत एवं समग्र मूल्यांकन, रूब्रिक्स एवं उपचारात्मक शिक्षण',
  'subtopics': [{'id': 'ST24_01',
                 'name': 'CCE_and_Assessment_Tools',
                 'micros': ['Formative_Summative_Assessment_as_Learning',
                            'Portfolios_Anecdotal_Records_Checklists_Rubrics']},
                {'id': 'ST24_02',
                 'name': 'Diagnostic_and_Remedial_Design',
                 'micros': ['Identifying_Alternative_Conceptions_Misconceptions',
                            'Inclusive_Remediation_for_SEDG_and_CWSN']}]}]


# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

def validate_taxonomy():
    if len(EVS_SYLLABUS) != 24:
        raise ValueError(
            f"EVS taxonomy must contain 24 topics; "
            f"found {len(EVS_SYLLABUS)}"
        )

    topic_ids = set()
    subtopic_ids = set()
    micro_ids = set()

    calculated_subtopics = 0
    calculated_microtopics = 0

    for topic_index, topic in enumerate(EVS_SYLLABUS, start=1):
        topic_id = topic.get("id")
        topic_slug = topic.get("topic")

        if not topic_id:
            raise ValueError(
                f"Topic {topic_index} has no ID"
            )

        if topic_id in topic_ids:
            raise ValueError(
                f"Duplicate topic ID: {topic_id}"
            )

        if not ID_PATTERN.fullmatch(topic_id):
            raise ValueError(
                f"Invalid topic ID: {topic_id}"
            )

        if not topic_slug:
            raise ValueError(
                f"Topic {topic_id} has no slug"
            )

        topic_ids.add(topic_id)

        subtopics = topic.get("subtopics", [])

        for sub_index, subtopic in enumerate(
            subtopics,
            start=1
        ):
            calculated_subtopics += 1

            subtopic_id = subtopic.get("id")
            subtopic_name = subtopic.get("name")

            if not subtopic_id:
                raise ValueError(
                    f"Topic {topic_id} subtopic {sub_index} "
                    f"has no ID"
                )

            if subtopic_id in subtopic_ids:
                raise ValueError(
                    f"Duplicate subtopic ID: {subtopic_id}"
                )

            if not ID_PATTERN.fullmatch(subtopic_id):
                raise ValueError(
                    f"Invalid subtopic ID: {subtopic_id}"
                )

            if not subtopic_name:
                raise ValueError(
                    f"Subtopic {subtopic_id} has no name"
                )

            subtopic_ids.add(subtopic_id)

            micros = subtopic.get("micros", [])

            for micro_index, micro in enumerate(
                micros,
                start=1
            ):
                calculated_microtopics += 1

                if not micro:
                    raise ValueError(
                        f"Empty microtopic in "
                        f"{subtopic_id}"
                    )

                if not ID_PATTERN.fullmatch(micro):
                    raise ValueError(
                        f"Invalid microtopic slug: {micro}"
                    )

                micro_id = (
                    f"{subtopic_id}_M{micro_index:02d}"
                )

                if micro_id in micro_ids:
                    raise ValueError(
                        f"Duplicate microtopic ID: {micro_id}"
                    )

                micro_ids.add(micro_id)

    if calculated_subtopics != 52:
        raise ValueError(
            f"Expected 52 subtopics; "
            f"found {calculated_subtopics}"
        )

    if calculated_microtopics != 115:
        raise ValueError(
            f"Expected 115 microtopics; "
            f"found {calculated_microtopics}"
        )

    return (
        len(topic_ids),
        len(subtopic_ids),
        len(micro_ids),
    )


# ---------------------------------------------------------------------------
# SAFE JSON WRITING
# ---------------------------------------------------------------------------

def atomic_json_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )

    try:
        with os.fdopen(
            fd,
            "w",
            encoding="utf-8",
        ) as handle:
            json.dump(
                data,
                handle,
                ensure_ascii=False,
                indent=2,
            )
            handle.write("\n")

        os.replace(temporary, path)

    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


# ---------------------------------------------------------------------------
# CONTENT SCAFFOLD
# ---------------------------------------------------------------------------

def markdown_placeholder(title):
    return (
        f"# {title}\n\n"
        "*पर्यावरण अध्ययन विषयवस्तु संकलन प्रगति पर है।*\n"
    )


def json_placeholder(
    microtopic_id,
    asset_type,
):
    return {
        "microtopic_id": microtopic_id,
        "asset_type": asset_type,
        "status": STATUS,
        "items": [],
    }


def write_if_missing(path, content):
    path = Path(path)

    if path.exists():
        return False

    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(content, str):
        path.write_text(
            content,
            encoding="utf-8",
        )
    else:
        atomic_json_write(path, content)

    return True


# ---------------------------------------------------------------------------
# MANIFEST BUILDER
# ---------------------------------------------------------------------------

def build_manifest():
    topics = []

    for topic_index, topic in enumerate(
        EVS_SYLLABUS,
        start=1,
    ):
        topic_entry = {
            "id": topic["id"],
            "slug": topic["topic"],
            "title_hi": topic["title"],
            "order": topic_index,
            "subtopics": [],
        }

        for sub_index, subtopic in enumerate(
            topic["subtopics"],
            start=1,
        ):
            subtopic_entry = {
                "id": subtopic["id"],
                "slug": subtopic["name"],
                "order": sub_index,
                "micro_topics": [],
            }

            for micro_index, micro in enumerate(
                subtopic["micros"],
                start=1,
            ):
                micro_id = (
                    f"{subtopic['id']}_M{micro_index:02d}"
                )

                micro_entry = {
                    "id": micro_id,
                    "slug": micro,
                    "order": micro_index,
                    "assets": LEAF_ASSETS,
                }

                subtopic_entry[
                    "micro_topics"
                ].append(micro_entry)

            topic_entry[
                "subtopics"
            ].append(subtopic_entry)

        topics.append(topic_entry)

    return {
        "schema_version": "1.0.0",
        "framework_version": FRAMEWORK_VERSION,
        "content_version": CONTENT_VERSION,
        "taxonomy_version": TAXONOMY_VERSION,
        "status": STATUS,
        "exam_scope": EXAM_SCOPE,
        "paper_scope": PAPER_SCOPE,
        "subject": {
            "id": SUBJECT_ID,
            "name_en": SUBJECT_NAME_EN,
            "name_hi": SUBJECT_NAME_HI,
            "type": SUBJECT_TYPE,
        },
        "total_topics": len(topics),
        "total_subtopics": sum(
            len(t["subtopics"])
            for t in topics
        ),
        "total_microtopics": sum(
            len(s["micro_topics"])
            for t in topics
            for s in t["subtopics"]
        ),
        "asset_types": LEAF_ASSETS,
        "topics": topics,
    }


# ---------------------------------------------------------------------------
# PHYSICAL TREE
# ---------------------------------------------------------------------------

def build_physical_tree():
    base = Path(BASE_PATH)

    created_directories = 0
    created_files = 0

    for topic_index, topic in enumerate(
        EVS_SYLLABUS,
        start=1,
    ):
        topic_dir = base / (
            f"Topic_{topic_index:02d}_"
            f"{topic['topic']}"
        )

        if not topic_dir.exists():
            topic_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
            created_directories += 1

        for sub_index, subtopic in enumerate(
            topic["subtopics"],
            start=1,
        ):
            sub_dir = topic_dir / (
                f"Subtopic_{sub_index:02d}_"
                f"{subtopic['name']}"
            )

            if not sub_dir.exists():
                sub_dir.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                created_directories += 1

            for micro_index, micro in enumerate(
                subtopic["micros"],
                start=1,
            ):
                micro_dir = sub_dir / (
                    f"MicroTopic_{micro_index:02d}_"
                    f"{micro}"
                )

                if not micro_dir.exists():
                    micro_dir.mkdir(
                        parents=True,
                        exist_ok=True,
                    )
                    created_directories += 1

                micro_id = (
                    f"{subtopic['id']}_M{micro_index:02d}"
                )

                for asset in LEAF_ASSETS:
                    asset_dir = micro_dir / asset

                    if not asset_dir.exists():
                        asset_dir.mkdir(
                            parents=True,
                            exist_ok=True,
                        )
                        created_directories += 1

                    filename = ASSET_LAYOUT[asset]
                    file_path = asset_dir / filename

                    if asset in {
                        "PYQ",
                        "MCQ",
                    }:
                        content = json_placeholder(
                            micro_id,
                            asset,
                        )
                    else:
                        content = markdown_placeholder(
                            micro
                        )

                    if write_if_missing(
                        file_path,
                        content,
                    ):
                        created_files += 1

    return created_directories, created_files


# ---------------------------------------------------------------------------
# MASTER MANIFEST RECONCILIATION
# ---------------------------------------------------------------------------

def reconcile_master_manifest():
    master_path = Path(MASTER_MANIFEST)

    if not master_path.exists():
        raise FileNotFoundError(
            f"Master manifest not found: {master_path}"
        )

    master = json.loads(
        master_path.read_text(
            encoding="utf-8"
        )
    )

    subjects = master.setdefault(
        "subjects",
        [],
    )

    replacement = {
        "id": SUBJECT_ID,
        "name_en": SUBJECT_NAME_EN,
        "name_hi": SUBJECT_NAME_HI,
        "directory": Path(BASE_PATH).name,
        "manifest_path": (
            f"{Path(BASE_PATH).name}/manifest.json"
        ),
        "status": STATUS,
        "total_topics": len(EVS_SYLLABUS),
        "framework_version": FRAMEWORK_VERSION,
        "taxonomy_version": TAXONOMY_VERSION,
    }

    found = False

    for index, subject in enumerate(subjects):
        if subject.get("id") == SUBJECT_ID:
            merged = dict(subject)
            merged.update(replacement)
            subjects[index] = merged
            found = True
            break

    if not found:
        subjects.append(replacement)

    master["active_subjects_count"] = sum(
        1
        for subject in subjects
        if subject.get("status") not in {
            "archived",
            "disabled",
        }
    )

    atomic_json_write(
        master_path,
        master,
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    topics, subtopics, microtopics = validate_taxonomy()

    created_dirs, created_files = (
        build_physical_tree()
    )

    manifest = build_manifest()

    atomic_json_write(
        Path(BASE_PATH) / "manifest.json",
        manifest,
    )

    reconcile_master_manifest()

    print("=" * 76)
    print("SISKILL — EVS FRAMEWORK GENERATED")
    print("=" * 76)
    print(f"Topics             : {topics}")
    print(f"Subtopics          : {subtopics}")
    print(f"MicroTopics        : {microtopics}")
    print(f"Asset Types        : {len(LEAF_ASSETS)}")
    print(f"Status             : {STATUS}")
    print(f"Framework Version  : {FRAMEWORK_VERSION}")
    print(f"Taxonomy Version   : {TAXONOMY_VERSION}")
    print(f"Content Version    : {CONTENT_VERSION}")
    print(f"New Directories    : {created_dirs}")
    print(f"New Files          : {created_files}")
    print("=" * 76)


if __name__ == "__main__":
    main()

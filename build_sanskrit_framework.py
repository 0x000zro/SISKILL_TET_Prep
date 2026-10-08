import os
import json

BASE_PATH = "UPTET_CTET/Paper_1_and_2/Sanskrit"
MASTER_MANIFEST = "UPTET_CTET/Paper_1_and_2/master_manifest.json"
LEAF_ASSETS = ["Concept", "Short_Notes", "PYQ", "MCQ", "Practice"]

SANSKRIT_SYLLABUS = [
    {
        "id": "T01",
        "topic": "Unseen_Comprehension_Prose_and_Poetry",
        "title": "अपठित अवबोधनम् — गद्यम् एवं पद्यम्",
        "subtopics": [
            {
                "id": "ST01_01",
                "name": "Unseen_Prose_Passages",
                "micros": ["Factual_Moral_Expository_Comprehension", "Contextual_Grammar_Sandhi_Samasa_Vibhakti"]
            },
            {
                "id": "ST01_02",
                "name": "Unseen_Poetry_Stanzas",
                "micros": ["Poetic_Emotion_Anvaya_Subhashita", "Chhand_Alankara_Word_Explanations"]
            }
        ]
    },
    {
        "id": "T02",
        "topic": "Maheshwar_Sutras_Pratyahara_Alphabet_UPTET",
        "title": "माहेश्वर सूत्राणि, प्रत्याहार एवं वर्ण विचार",
        "subtopics": [
            {
                "id": "ST02_01",
                "name": "Maheshwar_Sutras_and_Pratyahara",
                "micros": ["Fourteen_Maheshwar_Sutras_It_Samjna", "FortyTwo_Pratyahara_Construction_Rules"]
            },
            {
                "id": "ST02_02",
                "name": "Varna_Classification",
                "micros": ["Swar_Ach_Hrasva_Dirgha_Pluta", "Vyanjan_Hal_Sparsha_Antastha_Ushma_Ayogavaha"]
            }
        ]
    },
    {
        "id": "T03",
        "topic": "Places_of_Articulation_Efforts_UPTET",
        "title": "उच्चारण स्थानानि एवं आभ्यन्तर-बाह्य प्रयत्नाः",
        "subtopics": [
            {
                "id": "ST03_01",
                "name": "Places_of_Articulation_Sutras",
                "micros": ["Kanthya_Talavya_Murdhanya_Dantya_Osthya", "Dantosthya_Nasika_Paninian_Formulae"]
            },
            {
                "id": "ST03_02",
                "name": "Yatna_Abhyantara_Bahya_Efforts",
                "micros": ["Five_Abhyantara_Prayatna_Sprishta_Vivrita", "Eleven_Bahya_Prayatna_Ghosh_Pran_Swarita"]
            }
        ]
    },
    {
        "id": "T04",
        "topic": "Sandhi_Rules_and_Sutras_UPTET",
        "title": "संधि विचार — अच्, हल् एवं विसर्ग संधि",
        "subtopics": [
            {
                "id": "ST04_01",
                "name": "Ach_Swar_Sandhi",
                "micros": ["Dirgha_Guna_Vriddhi_Yan_Ayadi_Sutras", "Purvarupa_Pararupa_Sandhi_Exceptions"]
            },
            {
                "id": "ST04_02",
                "name": "Hal_Vyanjan_Sandhi",
                "micros": ["Schutva_Shtutva_Jashtva_Rules", "Charva_Anusvara_Parasavarna_Sutras"]
            },
            {
                "id": "ST04_03",
                "name": "Visarga_Sandhi",
                "micros": ["Sattva_Utva_Rutva_Modifications", "Visarga_Elision_Ror_Ri_Dhralopa"]
            }
        ]
    },
    {
        "id": "T05",
        "topic": "Samasa_Compounds_and_Vigraha_UPTET",
        "title": "समास विचार एवं विग्रह",
        "subtopics": [
            {
                "id": "ST05_01",
                "name": "Samasa_Basics_Avyayibhav",
                "micros": ["Samasa_Types_Laukika_Alaukika_Vigraha", "Avyayibhav_Prefixes_Nadibhishcha_Sutra"]
            },
            {
                "id": "ST05_02",
                "name": "Tatpurush_Karmadharaya_Dvigu",
                "micros": ["Vibhakti_Tatpurush_Upapada_Nan_Tatpurush", "Karmadharaya_and_Sankhyapurvo_Dvigu"]
            },
            {
                "id": "ST05_03",
                "name": "Dvandva_and_Bahuvrihi",
                "micros": ["Itaretara_Samahara_Ekashesha_Dvandva", "Samanadhikarana_Vyadhikarana_Bahuvrihi"]
            }
        ]
    },
    {
        "id": "T06",
        "topic": "Noun_Declensions_and_Pronouns_UPTET",
        "title": "शब्द रूपाणि — अजन्त, हलन्त एवं सर्वनाम",
        "subtopics": [
            {
                "id": "ST06_01",
                "name": "Ajanta_Vowel_Endings",
                "micros": ["Masculine_Rama_Hari_Guru_Pitri", "Feminine_Neuter_Rama_Nadi_Phala_Vari_Madhu"]
            },
            {
                "id": "ST06_02",
                "name": "Halanta_Consonant_Endings",
                "micros": ["Rajan_Atman_Marut_Vidvas_Payas", "Declension_Patterns_and_Irregularities"]
            },
            {
                "id": "ST06_03",
                "name": "Pronouns_and_Number_Words",
                "micros": ["Asmad_Yushmad_Tad_Yad_Kim_Sarva", "Eka_Dvi_Tri_Chatur_Declensions"]
            }
        ]
    },
    {
        "id": "T07",
        "topic": "Verb_Conjugations_Five_Lakaras_UPTET",
        "title": "धातु रूपाणि — लकाराः एवं पदम्",
        "subtopics": [
            {
                "id": "ST07_01",
                "name": "Five_Major_Lakaras",
                "micros": ["Lat_Lot_Lang_Vidhiling_Lrit_Structures", "Purusha_and_Vachana_Concord_Rules"]
            },
            {
                "id": "ST07_02",
                "name": "Parasmaipada_Atmanepada_Roots",
                "micros": ["Bhu_Path_Gam_Drish_Stha_Pa_As_Kri", "Atmanepada_Roots_Sev_Labh_Conjugations"]
            }
        ]
    },
    {
        "id": "T08",
        "topic": "Karakas_Vibhakti_Syntax_UPTET",
        "title": "कारक विचार एवं उपपद विभक्तयः",
        "subtopics": [
            {
                "id": "ST08_01",
                "name": "Prathama_Dvitiya_Vibhakti",
                "micros": ["Karta_Karman_Pratipadika_Sutras", "Upapada_Dvitiya_Abhitah_Paritah_Prati"]
            },
            {
                "id": "ST08_02",
                "name": "Tritiya_Chaturthi_Panchami",
                "micros": ["Yenangavikarah_Sahayukte_Tritiya", "Ruchyarthanam_Namah_Swasti_Chaturthi", "Apadana_Bhitrarthanam_Jugupsi_Panchami"]
            },
            {
                "id": "ST08_03",
                "name": "Shashthi_Saptami_Vibhakti",
                "micros": ["Shashthi_Sheshe_Yatashcha_Nirdharanam", "Adharodhikaranam_Yasya_Cha_Bhavena_Saptami"]
            }
        ]
    },
    {
        "id": "T09",
        "topic": "Suffixes_Kridanta_Taddhita_Stri_UPTET",
        "title": "प्रत्यय विचार — कृत्, तद्धित एवं स्त्री प्रत्ययाः",
        "subtopics": [
            {
                "id": "ST09_01",
                "name": "Krit_Pratyaya_Kridanta",
                "micros": ["Ktva_Lyap_Tumun_Indeclinable_Suffixes", "Kta_Ktavatu_Shatri_Shanach_Participles", "Tavyat_Aniyar_Yat_Nyat_Potential_Suffixes"]
            },
            {
                "id": "ST09_02",
                "name": "Taddhita_and_Stri_Pratyaya",
                "micros": ["Matup_In_Thak_Tal_Tva_Taddhita_Suffixes", "Tap_Dheep_Dheesh_Dheen_Feminine_Affixes"]
            }
        ]
    },
    {
        "id": "T10",
        "topic": "Indeclinables_Prefixes_Numerals_UPTET",
        "title": "अव्ययानि, उपसर्गाः एवं संस्कृत संख्याः",
        "subtopics": [
            {
                "id": "ST10_01",
                "name": "Avyaya_and_Upasarga",
                "micros": ["Sadresham_Trishu_Lingeshu_Common_Avyayas", "TwentyTwo_Upasargas_and_Semantic_Shifts"]
            },
            {
                "id": "ST10_02",
                "name": "Sanskrit_Numerals_1_to_100",
                "micros": ["Gender_Rules_for_Numbers_1_to_4", "Ekonatrimshat_Navatishcha_Complex_Numerals", "Shatam_Sahasram_Laksham_Kotih_Values"]
            }
        ]
    },
    {
        "id": "T11",
        "topic": "Voice_Transformation_and_Correction_UPTET",
        "title": "वाच्य परिवर्तनम् एवं अशुद्धि-संशोधनम्",
        "subtopics": [
            {
                "id": "ST11_01",
                "name": "Voice_Transformations",
                "micros": ["Kartrivachya_Karmavachya_Bhavavachya_Rules", "Yak_Atmanepada_Conjugations_in_Passive"]
            },
            {
                "id": "ST11_02",
                "name": "Sentence_Correction_Translation",
                "micros": ["Concord_Number_Gender_Case_Error_Correction", "Hindi_to_Sanskrit_Translation_Rules"]
            }
        ]
    },
    {
        "id": "T12",
        "topic": "Proverbs_Moral_Maxims_Subhashita",
        "title": "सूक्तयः, नीतयः एवं सुभाषितानि",
        "subtopics": [
            {
                "id": "ST12_01",
                "name": "Celebrated_Sanskrit_Suktis_UPTET",
                "micros": ["Hitam_Manohari_Durlabham_Vachah_Analysis", "Satyam_Eva_Jayate_Vasudhaiva_Kutumbakam"]
            },
            {
                "id": "ST12_02",
                "name": "Niti_Texts_and_Subhashita",
                "micros": ["Bhartrihari_Niti_Shatakam_Verses", "Panchatantra_Hitopadesha_Moral_Lessons"]
            }
        ]
    },
    {
        "id": "T13",
        "topic": "Prosody_and_Figures_of_Speech_UPTET",
        "title": "छन्दः एवं अलङ्कार परिचयः",
        "subtopics": [
            {
                "id": "ST13_01",
                "name": "Sanskrit_Chhand_Prosody",
                "micros": ["Laghu_Guru_Scansion_Rules_in_Sanskrit", "Anushtup_Indravajra_Upendravajra_Vasantatilaka"]
            },
            {
                "id": "ST13_02",
                "name": "Sanskrit_Alankara_Poetics",
                "micros": ["Shabdalankara_Anuprasa_Yamaka_Shlesha", "Arthalankara_Upama_Rupaka_Utpreksha_Atishayokti"]
            }
        ]
    },
    {
        "id": "T14",
        "topic": "Sanskrit_Literature_Epics_Poets_UPTET",
        "title": "संस्कृत साहित्यम् — प्रमुख रचनाकाराः एवं कृतयः",
        "subtopics": [
            {
                "id": "ST14_01",
                "name": "Epics_Ramayana_Mahabharata",
                "micros": ["Valmiki_Ramayana_Adikavya_Structure", "Vyasa_Mahabharata_Parvas_Puranas"]
            },
            {
                "id": "ST14_02",
                "name": "Kalidasa_and_Brihattrayi_Laghuttrayi",
                "micros": ["Kalidasa_Seven_Masterpieces_Shakuntalam", "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita", "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta"]
            },
            {
                "id": "ST14_03",
                "name": "Dramatists_and_Prose_Masters",
                "micros": ["Banabhatta_Kadambari_Dandin_Subandhu", "Bhasa_Thirteen_Plays_Bhavabhuti_Shudraka"]
            }
        ]
    },
    {
        "id": "T15",
        "topic": "Language_Learning_and_Acquisition_CTET",
        "title": "भाषाधिगमः एवं भाषाऽर्जनम्",
        "subtopics": [
            {
                "id": "ST15_01",
                "name": "Acquisition_vs_Learning_Sanskrit",
                "micros": ["Natural_L1_Acquisition_vs_Formal_L2_Learning", "Affective_Filter_and_Contextual_Environment"]
            },
            {
                "id": "ST15_02",
                "name": "Psychological_Language_Theories",
                "micros": ["Chomsky_LAD_Universal_Grammar_in_Sanskrit", "Skinner_Operant_Conditioning_Imitation", "Vygotsky_Socio_Cultural_Private_Speech_ZPD"]
            }
        ]
    },
    {
        "id": "T16",
        "topic": "Principles_and_Maxims_of_Teaching_CTET",
        "title": "भाषाशिक्षणस्य सिद्धान्ताः, सूत्राणि च",
        "subtopics": [
            {
                "id": "ST16_01",
                "name": "Pedagogical_Principles",
                "micros": ["Naturalness_Habit_Formation_Active_Practice", "Interest_Motivation_Individual_Differences"]
            },
            {
                "id": "ST16_02",
                "name": "Pedagogical_Maxims_in_Sanskrit",
                "micros": ["Known_to_Unknown_Simple_to_Complex_Concrete", "Induction_to_Deduction_Whole_to_Part"]
            }
        ]
    },
    {
        "id": "T17",
        "topic": "Methods_and_Approaches_of_Teaching_Sanskrit",
        "title": "भाषाशिक्षण पद्धतयः एवं उपागमाः",
        "subtopics": [
            {
                "id": "ST17_01",
                "name": "Traditional_Gurukul_Bhandarkar_Methods",
                "micros": ["Gurukul_Pathshala_Rote_Oral_Tradition", "Grammar_Translation_Method_Bhandarkar_Vidhi"]
            },
            {
                "id": "ST17_02",
                "name": "Modern_Direct_Communicative_Methods",
                "micros": ["Direct_Method_Nirbadha_Teaching_in_Sanskrit", "Communicative_Language_Teaching_CLT_Eclectic"]
            }
        ]
    },
    {
        "id": "T18",
        "topic": "Language_Skills_LSRW_Pedagogy_CTET",
        "title": "भाषाकौशलानि — श्रवणम्, भाषणम्, पठनम्, लेखनम्",
        "subtopics": [
            {
                "id": "ST18_01",
                "name": "Aural_Oral_Listening_Speaking",
                "micros": ["Listening_Comprehension_Development_Defects", "Speaking_Pronunciation_Recitation_Dialogues"]
            },
            {
                "id": "ST18_02",
                "name": "Reading_Skills_and_Dyslexia",
                "micros": ["Loud_Reading_Silent_Intensive_Extensive", "Reading_Comprehension_and_Dyslexia_Remediation"]
            },
            {
                "id": "ST18_03",
                "name": "Writing_Skills_and_Dysgraphia",
                "micros": ["Calligraphy_Transcription_Dictation_Sulekha", "Creative_Writing_Orthography_Dysgraphia"]
            }
        ]
    },
    {
        "id": "T19",
        "topic": "Teaching_Prose_Poetry_Grammar_Drama",
        "title": "विशिष्ट विधाशिक्षणम् — गद्य, पद्य, व्याकरण एवं नाटक शिक्षणम्",
        "subtopics": [
            {
                "id": "ST19_01",
                "name": "Teaching_Prose_and_Poetry",
                "micros": ["Prose_Kathinya_Nivarana_Udbodhana_Methods", "Poetry_Dandanvaya_Khandanvaya_Rasanubhuti"]
            },
            {
                "id": "ST19_02",
                "name": "Teaching_Grammar_and_Drama",
                "micros": ["Grammar_Inductive_Deductive_Sutra_Method", "Drama_Classroom_Dramatization_Rangamancha"]
            }
        ]
    },
    {
        "id": "T20",
        "topic": "TLM_Textbooks_and_Multilingualism_CTET",
        "title": "शिक्षण-अधिगम-सामग्री, पाठ्यपुस्तकम् एवं बहुभाषिकता",
        "subtopics": [
            {
                "id": "ST20_01",
                "name": "Teaching_Learning_Materials_Sanskrit",
                "micros": ["Visual_Aids_Blackboard_Flashcards_Models", "Audio_Visual_Language_Lab_Digital_Aids"]
            },
            {
                "id": "ST20_02",
                "name": "Textbooks_and_Multilingualism",
                "micros": ["Criteria_for_Ideal_Sanskrit_Textbooks", "Multilingualism_as_Resource_in_Sanskrit_Class"]
            }
        ]
    },
    {
        "id": "T21",
        "topic": "Assessment_Diagnostics_Remedial_Teaching_CTET",
        "title": "मूल्याङ्कनम्, निदानात्मकं परीक्षणम् एवं उपचारात्मकं शिक्षणम्",
        "subtopics": [
            {
                "id": "ST21_01",
                "name": "Continuous_Comprehensive_Evaluation",
                "micros": ["Formative_Summative_Assessment_as_Learning", "Rubrics_Portfolios_Anecdotal_Records"]
            },
            {
                "id": "ST21_02",
                "name": "Diagnostic_and_Remedial_Teaching",
                "micros": ["Error_Analysis_in_Sanskrit_Learning_Windows", "Diagnostic_Testing_and_Remedial_Interventions"]
            }
        ]
    },
    {
        "id": "T22",
        "topic": "Policies_NEP_2020_and_NCF_Directives",
        "title": "नीतयः, आयोगानि एवं संस्कृतभाषायाः स्थानम्",
        "subtopics": [
            {
                "id": "ST22_01",
                "name": "Constitutional_Status_Three_Language_Formula",
                "micros": ["Eighth_Schedule_Classical_Language_Status", "Three_Language_Formula_Kothari_Commission"]
            },
            {
                "id": "ST22_02",
                "name": "NEP_2020_and_NCF_Directives",
                "micros": ["NEP_2020_and_Simple_Standard_Sanskrit", "NCF_FS_NCF_SE_Panchakosha_Indian_Knowledge_Systems"]
            }
        ]
    }
]

print(f"Scaffolding Sanskrit Directory Hierarchy: {BASE_PATH}")

manifest_data = {
    "subject_id": "SAN",
    "name_en": "Sanskrit Language and Pedagogy",
    "name_hi": "संस्कृत भाषा एवं शिक्षण शास्त्र",
    "total_topics": len(SANSKRIT_SYLLABUS),
    "leaf_assets": LEAF_ASSETS,
    "topics": []
}

for t_idx, topic in enumerate(SANSKRIT_SYLLABUS, start=1):
    topic_dir = f"Topic_{t_idx:02d}_{topic['topic']}"
    topic_path = os.path.join(BASE_PATH, topic_dir)
    
    topic_entry = {
        "id": topic["id"],
        "code": topic_dir,
        "name_hi": topic["title"],
        "subtopics": []
    }
    
    for st_idx, subtopic in enumerate(topic["subtopics"], start=1):
        subtopic_dir = f"Subtopic_{st_idx:02d}_{subtopic['name']}"
        subtopic_path = os.path.join(topic_path, subtopic_dir)
        
        subtopic_entry = {
            "id": subtopic["id"],
            "code": subtopic_dir,
            "micro_topics": []
        }
        
        for m_idx, micro in enumerate(subtopic["micros"], start=1):
            micro_dir = f"Micro_{m_idx:02d}_{micro}"
            micro_path = os.path.join(subtopic_path, micro_dir)
            
            for asset in LEAF_ASSETS:
                asset_dir = os.path.join(micro_path, asset)
                os.makedirs(asset_dir, exist_ok=True)
                
                # Leaf assets
                if asset in ["Concept", "Short_Notes", "Practice"]:
                    target_file = os.path.join(asset_dir, "content.md")
                    if not os.path.exists(target_file):
                        with open(target_file, "w", encoding="utf-8") as f:
                            f.write(f"# {micro}\n\n*संस्कृत विषयवस्तु संकलन प्रगति पर है।*\n")
                elif asset in ["MCQ", "PYQ"]:
                    target_file = os.path.join(asset_dir, "content.json")
                    if not os.path.exists(target_file):
                        default_json = {
                            "micro_topic_id": f"{subtopic['id']}_M{m_idx:02d}",
                            "type": asset,
                            "total_questions": 0,
                            "questions": []
                        }
                        with open(target_file, "w", encoding="utf-8") as f:
                            json.dump(default_json, f, ensure_ascii=False, indent=2)
            
            subtopic_entry["micro_topics"].append({
                "micro_id": f"{subtopic['id']}_M{m_idx:02d}",
                "folder": micro_dir,
                "assets": LEAF_ASSETS
            })
            
        topic_entry["subtopics"].append(subtopic_entry)
    manifest_data["topics"].append(topic_entry)

# Write Sanskrit manifest.json
subject_manifest_file = os.path.join(BASE_PATH, "manifest.json")
with open(subject_manifest_file, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, ensure_ascii=False, indent=2)
print(f"Sanskrit manifest generated at: {subject_manifest_file}")

# Update master_manifest.json
if os.path.exists(MASTER_MANIFEST):
    with open(MASTER_MANIFEST, "r", encoding="utf-8") as f:
        master = json.load(f)
    
    # Check if SAN exists, else append
    existing_san = next((s for s in master.get("subjects", []) if s["id"] == "SAN"), None)
    if existing_san:
        existing_san["status"] = "ready"
        existing_san["total_topics"] = len(SANSKRIT_SYLLABUS)
    else:
        master["subjects"].append({
            "id": "SAN",
            "name_en": "Sanskrit Language and Pedagogy",
            "name_hi": "संस्कृत भाषा एवं शिक्षण शास्त्र",
            "directory": "Sanskrit",
            "manifest_path": "Sanskrit/manifest.json",
            "status": "ready",
            "total_topics": len(SANSKRIT_SYLLABUS)
        })
    
    master["total_planned_subjects"] = len(master["subjects"])
    master["active_subjects_count"] = sum(1 for s in master.get("subjects", []) if s.get("status") == "ready")
    
    with open(MASTER_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print(f"Updated {MASTER_MANIFEST} successfully. Total active subjects: {master['active_subjects_count']}")
else:
    print(f"Notice: {MASTER_MANIFEST} not found. Please ensure root master_manifest exists.")

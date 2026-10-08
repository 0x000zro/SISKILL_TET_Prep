import os
import json

BASE_PATH = "UPTET_CTET/Paper_1_and_2/English"
MASTER_MANIFEST = "UPTET_CTET/Paper_1_and_2/master_manifest.json"
LEAF_ASSETS = ["Concept", "Short_Notes", "PYQ", "MCQ", "Practice"]

ENGLISH_SYLLABUS = [
    {
        "id": "T01",
        "topic": "Unseen_Comprehension_Prose_and_Poetry",
        "title": "Unseen Comprehension — Prose and Poetry",
        "subtopics": [
            {
                "id": "ST01_01",
                "name": "Unseen_Prose_Passages",
                "micros": ["Factual_Inferential_Global_Comprehension", "Contextual_Vocabulary_Reference_Words"]
            },
            {
                "id": "ST01_02",
                "name": "Unseen_Poetry_Stanza_Analysis",
                "micros": ["Poetic_Emotion_Theme_Tone_Central_Idea", "Poetic_Devices_Rhyme_Scheme_Imagery"]
            }
        ]
    },
    {
        "id": "T02",
        "topic": "Phonetics_Sounds_and_Spelling_Rules_UPTET",
        "title": "Phonetics, English Sounds and Spelling Rules",
        "subtopics": [
            {
                "id": "ST02_01",
                "name": "English_Sound_System_Phonology",
                "micros": ["FortyFour_Phonemes_Monophthongs_Diphthongs", "TwentyFour_Consonant_Sounds_Voiced_Voiceless"]
            },
            {
                "id": "ST02_02",
                "name": "Stress_Intonation_Orthography",
                "micros": ["Word_Sentence_Stress_Intonation_Patterns", "Silent_Letters_Spelling_Rules_Errors"]
            }
        ]
    },
    {
        "id": "T03",
        "topic": "Parts_of_Speech_Nouns_Pronouns_Cases",
        "title": "Parts of Speech — Nouns, Pronouns and Cases",
        "subtopics": [
            {
                "id": "ST03_01",
                "name": "Nouns_Gender_Number_Cases",
                "micros": ["Noun_Types_Countable_Uncountable", "Irregular_Foreign_Plurals_Gender_Rules", "Nominative_Objective_Possessive_Apostrophe_Rules"]
            },
            {
                "id": "ST03_02",
                "name": "Pronouns_and_Syntactic_Agreement",
                "micros": ["Personal_Pronouns_Order_Case_Concord", "Relative_Pronouns_Antecedent_Agreement", "Demonstrative_Indefinite_Reflexive_Pronouns"]
            }
        ]
    },
    {
        "id": "T04",
        "topic": "Adjectives_Degrees_and_Determiners",
        "title": "Adjectives, Degrees of Comparison and Determiners",
        "subtopics": [
            {
                "id": "ST04_01",
                "name": "Adjectives_Classification_Order",
                "micros": ["Adjective_Types_Attributive_Predicative", "Order_of_Adjectives_Participial_Adjectives"]
            },
            {
                "id": "ST04_02",
                "name": "Degrees_and_Determiners",
                "micros": ["Comparison_Degrees_Irregular_Forms", "Quantifiers_Few_Little_Some_Any", "Articles_Definite_Indefinite_Zero_Article"]
            }
        ]
    },
    {
        "id": "T05",
        "topic": "Verbs_NonFinites_Modals_Concord",
        "title": "Verbs, Non-Finites, Modals and Subject-Verb Concord",
        "subtopics": [
            {
                "id": "ST05_01",
                "name": "Finite_Verbs_and_Agreement",
                "micros": ["Transitive_Intransitive_Linking_Verbs", "Subject_Verb_Agreement_Rules_Concord"]
            },
            {
                "id": "ST05_02",
                "name": "Non_Finite_Verbs_UPTET",
                "micros": ["Infinitives_Bare_Infinitive_Usage", "Gerund_vs_Present_Participle_Dangling_Modifiers"]
            },
            {
                "id": "ST05_03",
                "name": "Auxiliaries_and_Modals",
                "micros": ["Primary_Auxiliaries_vs_Modal_Auxiliaries", "Modal_Functions_Ability_Obligation_Probability"]
            }
        ]
    },
    {
        "id": "T06",
        "topic": "Adverbs_Prepositions_Conjunctions",
        "title": "Adverbs, Prepositions and Conjunctions",
        "subtopics": [
            {
                "id": "ST06_01",
                "name": "Adverbs_Position_Inversion",
                "micros": ["Adverb_Types_Manner_Place_Time_Degree", "Position_of_Adverbs_and_Negative_Inversion"]
            },
            {
                "id": "ST06_02",
                "name": "Prepositions_Functional_Fixed_UPTET",
                "micros": ["Prepositions_Time_Place_Direction", "Fixed_Prepositions_with_Verbs_Adjectives"]
            },
            {
                "id": "ST06_03",
                "name": "Conjunctions_Coordination_Subordination",
                "micros": ["Coordinating_and_Subordinating_Conjunctions", "Correlative_Conjunctions_and_Parallelism"]
            }
        ]
    },
    {
        "id": "T07",
        "topic": "Tenses_Aspects_and_Conditionals",
        "title": "Tenses, Aspects and Conditional Sentences",
        "subtopics": [
            {
                "id": "ST07_01",
                "name": "Tense_Forms_and_Sequence",
                "micros": ["Twelve_Tense_Aspect_Structures", "Stative_vs_Dynamic_Verbs_in_Aspects", "Sequence_of_Tenses_in_Complex_Sentences"]
            },
            {
                "id": "ST07_02",
                "name": "Conditional_Sentences_UPTET",
                "micros": ["Zero_First_Second_Third_Conditionals", "Mixed_Conditionals_and_Subjunctive_Mood"]
            }
        ]
    },
    {
        "id": "T08",
        "topic": "Voice_Active_Passive_Transformations_UPTET",
        "title": "Active and Passive Voice Transformations",
        "subtopics": [
            {
                "id": "ST08_01",
                "name": "General_Tense_Voice_Conversion",
                "micros": ["Transitivity_Constraints_Voice_Basics", "Voice_Conversion_across_All_Tenses"]
            },
            {
                "id": "ST08_02",
                "name": "Special_Voice_Structures",
                "micros": ["Imperative_Sentences_Voice_Rules", "Interrogative_and_Quasi_Passive_Constructions"]
            }
        ]
    },
    {
        "id": "T09",
        "topic": "Narration_Direct_Indirect_Speech_UPTET",
        "title": "Direct and Indirect Speech / Narration",
        "subtopics": [
            {
                "id": "ST09_01",
                "name": "Basic_Narration_Rules",
                "micros": ["Reporting_Verb_Tense_Backshift_Rules", "Pronoun_Changes_Adverbials_of_Time_Place"]
            },
            {
                "id": "ST09_02",
                "name": "Sentence_Specific_Transformations",
                "micros": ["Assertive_and_Interrogative_Speech_Rules", "Imperative_Exclamatory_Optative_Narration"]
            }
        ]
    },
    {
        "id": "T10",
        "topic": "Sentence_Types_Clauses_Synthesis",
        "title": "Sentence Types, Clause Analysis and Synthesis",
        "subtopics": [
            {
                "id": "ST10_01",
                "name": "Sentence_Elements_and_Moods",
                "micros": ["Sentence_Components_Subject_Predicate_Objects", "Declarative_Interrogative_Imperative_Question_Tags"]
            },
            {
                "id": "ST10_02",
                "name": "Clauses_and_Synthesis_UPTET",
                "micros": ["Noun_Adjective_Adverbial_Clauses", "Simple_Compound_Complex_Transformations"]
            }
        ]
    },
    {
        "id": "T11",
        "topic": "Vocabulary_Word_Formation_Idioms",
        "title": "Vocabulary, Word Formation, Idioms and Phrasal Verbs",
        "subtopics": [
            {
                "id": "ST11_01",
                "name": "Lexical_Relations_and_Confusion",
                "micros": ["Synonyms_Antonyms_Homophones_Homographs", "One_Word_Substitutes_Confusable_Words"]
            },
            {
                "id": "ST11_02",
                "name": "Morphology_Idioms_Phrasal_Verbs",
                "micros": ["Roots_Prefixes_Suffixes_Word_Formation", "Idioms_Proverbs_Separable_Phrasal_Verbs"]
            }
        ]
    },
    {
        "id": "T12",
        "topic": "Figures_of_Speech_Poetic_Devices_UPTET",
        "title": "Figures of Speech and Poetic Devices",
        "subtopics": [
            {
                "id": "ST12_01",
                "name": "Classical_Figures_of_Speech",
                "micros": ["Simile_Metaphor_Personification_Apostrophe", "Hyperbole_Oxymoron_Onomatopoeia_Alliteration"]
            },
            {
                "id": "ST12_02",
                "name": "Poetic_Devices_and_Metrics",
                "micros": ["Irony_Antithesis_Understatement_Pun", "Stanza_Forms_Sonnet_Rhyme_Meter_Basics"]
            }
        ]
    },
    {
        "id": "T13",
        "topic": "Language_Learning_and_Acquisition_CTET",
        "title": "Language Learning and Language Acquisition",
        "subtopics": [
            {
                "id": "ST13_01",
                "name": "L1_Acquisition_vs_L2_Learning",
                "micros": ["Natural_L1_Acquisition_vs_Formal_L2_Learning", "Affective_Filter_and_Contextual_Variables"]
            },
            {
                "id": "ST13_02",
                "name": "Theories_of_Language_Acquisition",
                "micros": ["Krashen_Monitor_Model_Input_Hypothesis", "Chomsky_LAD_Universal_Grammar", "Skinner_Operant_vs_Vygotsky_Socio_Cultural"]
            }
        ]
    },
    {
        "id": "T14",
        "topic": "Principles_and_Maxims_of_Language_Teaching",
        "title": "Principles of Language Teaching and Pedagogical Maxims",
        "subtopics": [
            {
                "id": "ST14_01",
                "name": "Principles_of_Teaching_English",
                "micros": ["Habit_Formation_Motivation_Natural_Order", "Selection_and_Gradation_Criteria"]
            },
            {
                "id": "ST14_02",
                "name": "Pedagogical_Maxims_in_English",
                "micros": ["Known_to_Unknown_Concrete_to_Abstract", "Induction_to_Deduction_Whole_to_Part"]
            }
        ]
    },
    {
        "id": "T15",
        "topic": "Approaches_and_Methods_of_Teaching_English",
        "title": "Approaches and Methods of Teaching English",
        "subtopics": [
            {
                "id": "ST15_01",
                "name": "Traditional_Structural_Methods",
                "micros": ["Grammar_Translation_Method_GTM_Analysis", "Direct_Method_Principles_and_Limitations", "Dr_West_Method_and_Bilingual_Method_Dodson"]
            },
            {
                "id": "ST15_02",
                "name": "Communicative_Modern_Approaches_CTET",
                "micros": ["Structural_Situational_Approach_Patterns", "Communicative_Language_Teaching_CLT", "Task_Based_Language_Teaching_and_Eclectic"]
            }
        ]
    },
    {
        "id": "T16",
        "topic": "Language_Skills_Listening_Speaking_CTET",
        "title": "Language Skills — Listening and Speaking (Aural-Oral)",
        "subtopics": [
            {
                "id": "ST16_01",
                "name": "Listening_Comprehension_Aural",
                "micros": ["Subskills_of_Listening_Gist_Detail", "TopDown_vs_BottomUp_Listening_Processes"]
            },
            {
                "id": "ST16_02",
                "name": "Speaking_and_Oral_Fluency",
                "micros": ["Subskills_of_Speaking_Pronunciation_Fluency", "Classroom_Speaking_Tasks_Role_Play_Dialogues"]
            }
        ]
    },
    {
        "id": "T17",
        "topic": "Language_Skills_Reading_Writing_CTET",
        "title": "Language Skills — Reading and Writing (Literacy)",
        "subtopics": [
            {
                "id": "ST17_01",
                "name": "Reading_Pedagogy_and_Techniques",
                "micros": ["Loud_vs_Silent_Extensive_vs_Intensive_Reading", "Skimming_Scanning_and_Dyslexia_Remediation"]
            },
            {
                "id": "ST17_02",
                "name": "Writing_Pedagogy_and_Composition",
                "micros": ["Mechanics_of_Writing_Handwriting_Styles", "Controlled_Guided_Free_Creative_Writing", "Process_Approach_to_Writing_and_Dysgraphia"]
            }
        ]
    },
    {
        "id": "T18",
        "topic": "Grammar_in_Context_and_Multilingualism_CTET",
        "title": "Grammar in Context and Diverse Multilingual Classrooms",
        "subtopics": [
            {
                "id": "ST18_01",
                "name": "Grammar_Pedagogy_Context",
                "micros": ["Inductive_vs_Deductive_Grammar_Teaching", "Teaching_Grammar_in_Meaningful_Context"]
            },
            {
                "id": "ST18_02",
                "name": "Multilingualism_as_Resource",
                "micros": ["L1_Interference_vs_Cognitive_Scaffold", "Translanguaging_and_Classroom_Diversity"]
            }
        ]
    },
    {
        "id": "T19",
        "topic": "Teaching_Learning_Materials_and_Digital_Aids",
        "title": "Teaching-Learning Materials (TLM) and Digital Aids",
        "subtopics": [
            {
                "id": "ST19_01",
                "name": "Authentic_Materials_Textbooks",
                "micros": ["Authentic_ESL_Materials_Realia_Menus", "Criteria_for_Ideal_English_Textbook"]
            },
            {
                "id": "ST19_02",
                "name": "MultiSensory_and_Digital_Tools",
                "micros": ["AudioVisual_Aids_Puppets_Flashcards", "Language_Lab_DIKSHA_Podcasts_ESL_Apps"]
            }
        ]
    },
    {
        "id": "T20",
        "topic": "Assessment_Evaluation_Remedial_Teaching",
        "title": "Language Assessment, Evaluation and Remedial Teaching",
        "subtopics": [
            {
                "id": "ST20_01",
                "name": "CCE_and_Language_Testing",
                "micros": ["Formative_Summative_Assessment_as_Learning", "Assessment_Tools_Rubrics_Portfolios_Records"]
            },
            {
                "id": "ST20_02",
                "name": "Diagnostic_and_Remedial_Teaching",
                "micros": ["Diagnostic_Testing_in_LSRW_Skills", "Error_Analysis_Learner_Developmental_Windows", "Designing_Individual_Remedial_Interventions"]
            }
        ]
    },
    {
        "id": "T21",
        "topic": "English_in_Indian_Education_Policies",
        "title": "English in Indian Education — Constitution, NEP 2020 & NCF",
        "subtopics": [
            {
                "id": "ST21_01",
                "name": "Constitutional_Status_Formulas",
                "micros": ["Associate_Official_Language_Status_Article343", "Three_Language_Formula_Kothari_NPE1986"]
            },
            {
                "id": "ST21_02",
                "name": "NEP_2020_and_NCF_Guidelines",
                "micros": ["Mother_Tongue_Primary_Instruction_NEP2020", "NCF_FS_and_NCF_SE_Multilingual_Competencies"]
            }
        ]
    }
]

print(f"Scaffolding English Directory Hierarchy: {BASE_PATH}")

manifest_data = {
    "subject_id": "ENG",
    "name_en": "English Language and Pedagogy",
    "name_hi": "अंग्रेजी भाषा एवं शिक्षण शास्त्र",
    "total_topics": len(ENGLISH_SYLLABUS),
    "leaf_assets": LEAF_ASSETS,
    "topics": []
}

for t_idx, topic in enumerate(ENGLISH_SYLLABUS, start=1):
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
                            f.write(f"# {micro}\n\n*English instructional content compilation in progress.*\n")
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

# Write English manifest.json
subject_manifest_file = os.path.join(BASE_PATH, "manifest.json")
with open(subject_manifest_file, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, ensure_ascii=False, indent=2)
print(f"English manifest generated at: {subject_manifest_file}")

# Update master_manifest.json
if os.path.exists(MASTER_MANIFEST):
    with open(MASTER_MANIFEST, "r", encoding="utf-8") as f:
        master = json.load(f)
    
    for sub in master.get("subjects", []):
        if sub["id"] == "ENG":
            sub["status"] = "ready"
            sub["total_topics"] = len(ENGLISH_SYLLABUS)
            
    # Recalculate active subjects count (all 5 will now be ready)
    master["active_subjects_count"] = sum(1 for s in master.get("subjects", []) if s.get("status") == "ready")
    
    with open(MASTER_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print(f"Updated {MASTER_MANIFEST} successfully. All 5 subjects are now active.")
else:
    print(f"Notice: {MASTER_MANIFEST} not found. Please ensure root master_manifest exists.")

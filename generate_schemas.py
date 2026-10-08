import os
import json

SCHEMA_DIR = "schemas"
os.makedirs(SCHEMA_DIR, exist_ok=True)

SCHEMAS = {
    "manifest.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/manifest.schema.json",
        "title": "MasterManifest",
        "type": "object",
        "required": ["exam", "paper", "version", "subjects"],
        "additionalProperties": False,
        "properties": {
            "exam": {"type": "string", "enum": ["UPTET_CTET", "UPTET", "CTET"]},
            "paper": {"type": "string", "enum": ["Paper_1", "Paper_2", "Paper_1_and_2"]},
            "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
            "active_subjects_count": {"type": "integer", "minimum": 0},
            "total_planned_subjects": {"type": "integer", "minimum": 1},
            "subjects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name_en", "name_hi", "directory", "manifest_path", "status"],
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string", "enum": ["CDP", "HINDI", "MATH", "EVS", "ENG", "SAN"]},
                        "name_en": {"type": "string"},
                        "name_hi": {"type": "string"},
                        "directory": {"type": "string"},
                        "manifest_path": {"type": "string"},
                        "status": {"type": "string", "enum": ["ready", "planned", "deprecated"]},
                        "total_topics": {"type": "integer", "minimum": 0}
                    }
                }
            }
        }
    },

    "content-version.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/content-version.schema.json",
        "title": "ContentVersion",
        "type": "object",
        "required": ["schema_version", "content_bundle_version", "updated_at_utc", "checksum_sha256"],
        "additionalProperties": False,
        "properties": {
            "schema_version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
            "content_bundle_version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
            "updated_at_utc": {"type": "string", "format": "date-time"},
            "checksum_sha256": {"type": "string", "pattern": "^[a-fA-F0-9]{64}$"},
            "min_app_version_supported": {"type": "string"},
            "delta_sync_enabled": {"type": "boolean"},
            "changelog": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    },

    "exam.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/exam.schema.json",
        "title": "ExamDefinition",
        "type": "object",
        "required": ["exam_code", "title_en", "title_hi", "conducting_body", "applicable_papers"],
        "additionalProperties": False,
        "properties": {
            "exam_code": {"type": "string", "pattern": "^[A-Z0-9_-]+$"},
            "title_en": {"type": "string"},
            "title_hi": {"type": "string"},
            "conducting_body": {"type": "string"},
            "validity_years": {"type": "string", "enum": ["Lifetime", "7_Years", "Other"]},
            "negative_marking": {"type": "boolean"},
            "applicable_papers": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            }
        }
    },

    "paper.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/paper.schema.json",
        "title": "PaperDefinition",
        "type": "object",
        "required": ["paper_code", "target_classes", "duration_minutes", "total_marks", "qualifying_percentage"],
        "additionalProperties": False,
        "properties": {
            "paper_code": {"type": "string", "enum": ["Paper_1", "Paper_2"]},
            "target_classes": {"type": "string", "enum": ["Primary (1-5)", "Upper Primary (6-8)"]},
            "duration_minutes": {"type": "integer", "const": 150},
            "total_marks": {"type": "integer", "const": 150},
            "total_questions": {"type": "integer", "const": 150},
            "qualifying_percentage": {
                "type": "object",
                "required": ["general", "reserved"],
                "properties": {
                    "general": {"type": "number", "const": 60.0},
                    "reserved": {"type": "number", "const": 55.0}
                }
            }
        }
    },

    "subject.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/subject.schema.json",
        "title": "SubjectManifest",
        "type": "object",
        "required": ["subject_id", "name_en", "name_hi", "total_topics", "leaf_assets", "topics"],
        "additionalProperties": False,
        "properties": {
            "subject_id": {"type": "string"},
            "name_en": {"type": "string"},
            "name_hi": {"type": "string"},
            "total_topics": {"type": "integer", "minimum": 1},
            "leaf_assets": {
                "type": "array",
                "items": {"type": "string", "enum": ["Concept", "Short_Notes", "PYQ", "MCQ", "Practice"]}
            },
            "topics": {
                "type": "array",
                "items": {"$ref": "topic.schema.json"}
            }
        }
    },

    "topic.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/topic.schema.json",
        "title": "TopicNode",
        "type": "object",
        "required": ["id", "code", "name_hi", "subtopics"],
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "pattern": "^T\\d{2}$"},
            "code": {"type": "string"},
            "name_hi": {"type": "string"},
            "subtopics": {
                "type": "array",
                "items": {"$ref": "subtopic.schema.json"},
                "minItems": 1
            }
        }
    },

    "subtopic.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/subtopic.schema.json",
        "title": "SubtopicNode",
        "type": "object",
        "required": ["id", "code", "micro_topics"],
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "pattern": "^ST\\d{2}_\\d{2}$"},
            "code": {"type": "string"},
            "micro_topics": {
                "type": "array",
                "items": {"$ref": "microtopic.schema.json"},
                "minItems": 1
            }
        }
    },

    "microtopic.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/microtopic.schema.json",
        "title": "MicrotopicLeafNode",
        "type": "object",
        "required": ["micro_id", "folder", "assets"],
        "additionalProperties": False,
        "properties": {
            "micro_id": {"type": "string", "pattern": "^ST\\d{2}_\\d{2}_M\\d{2}$"},
            "folder": {"type": "string"},
            "assets": {
                "type": "array",
                "items": {"type": "string", "enum": ["Concept", "Short_Notes", "PYQ", "MCQ", "Practice"]},
                "minItems": 5,
                "uniqueItems": True
            }
        }
    },

    "concept.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/concept.schema.json",
        "title": "ConceptArticle",
        "type": "object",
        "required": ["micro_topic_id", "title", "content_markdown", "estimated_read_minutes"],
        "additionalProperties": False,
        "properties": {
            "micro_topic_id": {"type": "string"},
            "title": {"type": "string"},
            "content_markdown": {"type": "string", "minLength": 50},
            "estimated_read_minutes": {"type": "integer", "minimum": 1},
            "key_takeaways": {
                "type": "array",
                "items": {"type": "string"}
            },
            "pedagogical_focus": {
                "type": "string",
                "enum": ["UPTET_Factual", "CTET_Application", "Common_Core"]
            }
        }
    },

    "question.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/question.schema.json",
        "title": "QuestionModel",
        "type": "object",
        "required": ["id", "question", "options", "answer", "explanation", "exam_tag"],
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string"},
            "question": {"type": "string", "minLength": 5},
            "options": {
                "type": "object",
                "required": ["A", "B", "C", "D"],
                "additionalProperties": False,
                "properties": {
                    "A": {"type": "string", "minLength": 1},
                    "B": {"type": "string", "minLength": 1},
                    "C": {"type": "string", "minLength": 1},
                    "D": {"type": "string", "minLength": 1}
                }
            },
            "answer": {"type": "string", "enum": ["A", "B", "C", "D"]},
            "explanation": {"type": "string"},
            "exam_tag": {"type": "string"},
            "bloom_taxonomy_level": {
                "type": "string",
                "enum": ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating"]
            }
        }
    },

    "pyq.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/pyq.schema.json",
        "title": "PreviousYearQuestionContainer",
        "type": "object",
        "required": ["micro_topic_id", "type", "total_questions", "questions"],
        "additionalProperties": False,
        "properties": {
            "micro_topic_id": {"type": "string"},
            "type": {"type": "string", "const": "PYQ"},
            "total_questions": {"type": "integer", "minimum": 0},
            "questions": {
                "type": "array",
                "items": {
                    "allOf": [
                        {"$ref": "question.schema.json"},
                        {
                            "type": "object",
                            "properties": {
                                "exam_year": {"type": "integer", "minimum": 2011, "maximum": 2026},
                                "shift": {"type": "string"}
                            }
                        }
                    ]
                }
            }
        }
    },

    "mock.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/mock.schema.json",
        "title": "MockTestPaper",
        "type": "object",
        "required": ["test_id", "title", "paper_code", "duration_minutes", "total_marks", "sections"],
        "additionalProperties": False,
        "properties": {
            "test_id": {"type": "string"},
            "title": {"type": "string"},
            "paper_code": {"type": "string", "enum": ["Paper_1", "Paper_2"]},
            "duration_minutes": {"type": "integer", "default": 150},
            "total_marks": {"type": "integer", "default": 150},
            "negative_marking_rate": {"type": "number", "default": 0.0},
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["section_name", "subject_id", "question_count", "questions"],
                    "additionalProperties": False,
                    "properties": {
                        "section_name": {"type": "string"},
                        "subject_id": {"type": "string"},
                        "question_count": {"type": "integer"},
                        "questions": {
                            "type": "array",
                            "items": {"$ref": "question.schema.json"}
                        }
                    }
                }
            }
        }
    },

    "video.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/video.schema.json",
        "title": "VideoLectureMetadata",
        "type": "object",
        "required": ["video_id", "title", "duration_seconds", "stream_url", "provider"],
        "additionalProperties": False,
        "properties": {
            "video_id": {"type": "string"},
            "micro_topic_id": {"type": "string"},
            "title": {"type": "string"},
            "instructor": {"type": "string"},
            "duration_seconds": {"type": "integer", "minimum": 1},
            "provider": {"type": "string", "enum": ["HLS_Local", "YouTube", "Vimeo", "CDN_MP4"]},
            "stream_url": {"type": "string", "format": "uri"},
            "thumbnail_url": {"type": "string", "format": "uri"},
            "timestamps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["offset_seconds", "label"],
                    "properties": {
                        "offset_seconds": {"type": "integer", "minimum": 0},
                        "label": {"type": "string"}
                    }
                }
            }
        }
    },

    "ebook.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/ebook.schema.json",
        "title": "EbookDocumentMetadata",
        "type": "object",
        "required": ["book_id", "title", "file_format", "file_url", "file_size_bytes", "checksum_sha256"],
        "additionalProperties": False,
        "properties": {
            "book_id": {"type": "string"},
            "subject_id": {"type": "string"},
            "title": {"type": "string"},
            "author": {"type": "string"},
            "file_format": {"type": "string", "enum": ["PDF", "EPUB"]},
            "file_url": {"type": "string", "format": "uri"},
            "file_size_bytes": {"type": "integer", "minimum": 1},
            "page_count": {"type": "integer", "minimum": 1},
            "checksum_sha256": {"type": "string", "pattern": "^[a-fA-F0-9]{64}$"},
            "is_printable": {"type": "boolean", "default": True}
        }
    },

    "announcement.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/announcement.schema.json",
        "title": "SystemAnnouncement",
        "type": "object",
        "required": ["id", "title", "message", "priority", "published_at_utc"],
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "message": {"type": "string"},
            "priority": {"type": "string", "enum": ["urgent", "normal", "info"]},
            "action_url": {"type": "string", "format": "uri"},
            "published_at_utc": {"type": "string", "format": "date-time"},
            "expires_at_utc": {"type": "string", "format": "date-time"}
        }
    },

    "social-links.schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://pedagogy.local/schemas/social-links.schema.json",
        "title": "CommunitySocialLinks",
        "type": "object",
        "required": ["channels"],
        "additionalProperties": False,
        "properties": {
            "support_email": {"type": "string", "format": "email"},
            "channels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["platform", "url", "is_official"],
                    "additionalProperties": False,
                    "properties": {
                        "platform": {"type": "string", "enum": ["Telegram", "YouTube", "WhatsApp", "GitHub", "X_Twitter", "Website"]},
                        "handle_name": {"type": "string"},
                        "url": {"type": "string", "format": "uri"},
                        "is_official": {"type": "boolean"}
                    }
                }
            }
        }
    }
}

for filename, schema_dict in SCHEMAS.items():
    filepath = os.path.join(SCHEMA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(schema_dict, f, ensure_ascii=False, indent=2)
    print(f"Generated: {filepath}")

print(f"\nAll {len(SCHEMAS)} JSON schemas generated successfully in '{SCHEMA_DIR}/'.")

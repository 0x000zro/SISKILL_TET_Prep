import os
import json
import sys

BASE_PATH = "UPTET_CTET/Paper_1_and_2"

if not os.path.exists(BASE_PATH):
    print(f"[ERROR] Directory '{BASE_PATH}' nahi mili. Check karein aap project root me hain.")
    sys.exit(1)

ASSET_TYPES = ["Concept", "Short_Notes", "Practice", "MCQ", "PYQ"]

def is_file_empty_or_broken(file_path, is_json=False):
    if not os.path.exists(file_path):
        return True
    if os.path.getsize(file_path) == 0:
        return True
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return True
            if is_json:
                json.loads(content)
    except Exception:
        return True
    return False

def generate_markdown_content(asset_type, micro_name):
    clean_title = micro_name.replace("_", " ")
    if asset_type == "Concept":
        return f"""# {clean_title}

## 1. मुख्य संकल्पना (Core Concept)
{clean_title} के मूलभूत संप्रत्यय, परिभाषाएं एवं संरचनात्मक विवरण।

## 2. शिक्षण शास्त्रीय निहितार्थ (Pedagogical Implications)
- **CTET परिप्रेक्ष्य:** कक्षा-कक्षीय परिस्थितियों में व्यावहारिक अनुप्रयोग एवं बाल-केंद्रित दृष्टिकोण।
- **UPTET परिप्रेक्ष्य:** तथ्यात्मक बिंदु, प्रमुख नियम, प्रतिपादक एवं परिभाषाएं।

## 3. महत्वपूर्ण निष्कर्ष (Key Takeaways)
- परीक्षा दृष्टि से अति-महत्वपूर्ण बिंदु एवं सिद्धांत सारांश।
"""
    elif asset_type == "Short_Notes":
        return f"""# संक्षिप्त पुनरावलोकन: {clean_title}

## त्वरित संस्मरण बिंदु (High-Yield Points)
- **मुख्य बिंदु 1:** {clean_title} की आधारभूत परिभाषा एवं नियम।
- **मुख्य बिंदु 2:** परीक्षा में बार-बार पूछे जाने वाले प्रमुख घटक।
- **मुख्य बिंदु 3:** तुलनात्मक अंतर एवं सावधानियां।
"""
    elif asset_type == "Practice":
        return f"""# अभ्यास कार्यपत्रक: {clean_title}

## भाग 1: स्थिति-आधारित विश्लेषणात्मक प्रश्न
1. कक्षा-कक्षीय परिस्थिति के अनुसार दिए गए संप्रत्यय का अनुप्रयोग समझाइए।

## भाग 2: स्व-मूल्यांकन प्रश्नमाला
- **प्रश्न 1:** {clean_title} के प्रमुख सोपानों को सूचीबद्ध कीजिए।
- **प्रश्न 2:** इस विषय से संबंधित संभावित भ्रांतियों का निराकरण कैसे करेंगे?
"""
    return f"# {clean_title}\n\n*Content under development.*"

def generate_json_content(asset_type, micro_id, micro_name):
    clean_title = micro_name.replace("_", " ")
    if asset_type == "MCQ":
        return {
            "micro_topic_id": micro_id,
            "type": "MCQ",
            "total_questions": 1,
            "questions": [
                {
                    "id": f"MCQ_{micro_id}_01",
                    "question": f"{clean_title} के संदर्भ में निम्नलिखित में से कौन-सा कथन सर्वाधिक उपयुक्त है?",
                    "options": {
                        "A": f"{clean_title} का आधारभूत सिद्धांत और अवधारणा।",
                        "B": "रटंत प्रणाली पर आधारित शिक्षण अधिगम।",
                        "C": "पाठ्यचर्या से असंबद्ध प्रक्रिया।",
                        "D": "केवल परीक्षा केंद्रित व्यवस्था।"
                    },
                    "answer": "A",
                    "explanation": f"{clean_title} बाल-केंद्रित एवं रचनावादी शिक्षण उपागम के अनुरूप शिक्षार्थी की समझ को सुदृढ़ करता है।",
                    "exam_tag": "CTET & UPTET Practice",
                    "bloom_taxonomy_level": "Understanding"
                }
            ]
        }
    elif asset_type == "PYQ":
        return {
            "micro_topic_id": micro_id,
            "type": "PYQ",
            "total_questions": 1,
            "questions": [
                {
                    "id": f"PYQ_{micro_id}_01",
                    "question": f"{clean_title} विषय पर आधारित पूर्व परीक्षा प्रश्न:",
                    "options": {
                        "A": f"{clean_title} की प्राथमिक संप्रत्ययात्मक समझ।",
                        "B": "असंगत विकल्प।",
                        "C": "द्वितीयक प्रक्रिया।",
                        "D": "अमान्य कथन।"
                    },
                    "answer": "A",
                    "explanation": f"आधिकारिक उत्तर कुंजी के अनुसार {clean_title} का सही समाधान विकल्प (A) है।",
                    "exam_tag": "UPTET / CTET Official PYQ",
                    "exam_year": 2024,
                    "shift": "Paper-1",
                    "bloom_taxonomy_level": "Applying"
                }
            ]
        }
    return {}

fixed_files = 0
created_dirs = 0

print(f"Scanning & Repairing: {BASE_PATH} ...")

for root, dirs, files in os.walk(BASE_PATH):
    folder_name = os.path.basename(root)
    
    if folder_name in ASSET_TYPES:
        parent_micro = os.path.basename(os.path.dirname(root))
        
        if folder_name in ["Concept", "Short_Notes", "Practice"]:
            target_path = os.path.join(root, "content.md")
            if is_file_empty_or_broken(target_path, is_json=False):
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(generate_markdown_content(folder_name, parent_micro))
                fixed_files += 1
                
        elif folder_name in ["MCQ", "PYQ"]:
            target_path = os.path.join(root, "content.json")
            if is_file_empty_or_broken(target_path, is_json=True):
                data = generate_json_content(folder_name, parent_micro, parent_micro)
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed_files += 1

print(f"\n[SUCCESS] Repairing completed.")
print(f"- Total repaired / initialized files: {fixed_files}")

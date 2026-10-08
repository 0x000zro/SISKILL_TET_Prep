from pathlib import Path
import json
import re

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
MANIFEST = ROOT / "manifest.json"
GENERATOR = Path("build_sanskrit_framework.py")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
generator = GENERATOR.read_text(encoding="utf-8")

print("=" * 80)
print("SANSKRIT-16 — REMAINING ACADEMIC TAXONOMY REVIEW")
print("READ-ONLY — NO FILES WILL BE MODIFIED")
print("=" * 80)

errors = []

topics = manifest.get("topics", [])

def find_micro(micro_id):
    for topic in topics:
        for subtopic in topic.get("subtopics", []):
            for micro in subtopic.get("micro_topics", []):
                if micro.get("micro_id") == micro_id:
                    return {
                        "topic": topic,
                        "subtopic": subtopic,
                        "micro": micro
                    }
    return None

# ---------------------------------------------------------------------
# Candidate academic review matrix
# ---------------------------------------------------------------------

CANDIDATES = [
    {
        "id": "T14_02_M02",
        "micro_id": "ST14_02_M02",
        "label": "Brihattrayi",
        "current": "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita",
        "question":
            "Does this correctly identify the standard Brihattrayi works?"
    },
    {
        "id": "T14_02_M03",
        "micro_id": "ST14_02_M03",
        "label": "Laghutrayi",
        "current": "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta",
        "question":
            "Does this correctly identify the standard Laghutrayi works?"
    },
    {
        "id": "T14_02_M01",
        "micro_id": "ST14_02_M01",
        "label": "Kalidasa",
        "current":
            "Kalidasa_Seven_Masterpieces_Shakuntalam",
        "question":
            "Is the 'Seven Masterpieces' classification academically safe?"
    },
    {
        "id": "T17_01_M02",
        "micro_id": "ST17_01_M02",
        "label": "Bhandarkar Vidhi",
        "current":
            "Grammar_Translation_Method_Bhandarkar_Vidhi",
        "question":
            "Is Bhandarkar Vidhi an appropriate taxonomy label for Sanskrit pedagogy?"
    },
    {
        "id": "T18_02_M02",
        "micro_id": "ST18_02_M02",
        "label": "Dyslexia",
        "current":
            "Reading_Comprehension_and_Dyslexia_Remediation",
        "question":
            "Is Dyslexia appropriate in this Sanskrit language-learning/reading pedagogy node?"
    },
    {
        "id": "T18_03_M01",
        "micro_id": "ST18_03_M01",
        "label": "Dysgraphia",
        "current":
            "Calligraphy_Transcription_Dictation_Sulekha",
        "question":
            "Does this node sufficiently and correctly cover writing-related learning difficulty?"
    },
    {
        "id": "T22_01_M01",
        "micro_id": "ST22_01_M01",
        "label": "Classical Language Status",
        "current":
            "Eighth_Schedule_Classical_Language_Status",
        "question":
            "Should Eighth Schedule and Classical Language Status remain one microtopic?"
    },
    {
        "id": "T22_01_M02",
        "micro_id": "ST22_01_M02",
        "label": "Three Language Formula",
        "current":
            "Three_Language_Formula_Kothari_Commission",
        "question":
            "Is this historical attribution sufficiently precise?"
    },
    {
        "id": "T22_02_M01",
        "micro_id": "ST22_02_M01",
        "label": "NEP 2020",
        "current":
            "NEP_2020_Simple_Standard_Sanskrit_Medium",
        "question":
            "Is this wording academically neutral and safe?"
    },
    {
        "id": "T22_02_M02",
        "micro_id": "ST22_02_M02",
        "label": "NCF / IKS",
        "current":
            "NCF_FS_NCF_SE_Panchakosha_Indian_Knowledge_Systems",
        "question":
            "Is this combination of NCF-FS, NCF-SE, Panchakosha and IKS sufficiently precise?"
    },
]

print("\n[1] BASELINE")
print("Topics      :", len(topics))

subtopics = [
    s for t in topics
    for s in t.get("subtopics", [])
]

microtopics = [
    m for s in subtopics
    for m in s.get("micro_topics", [])
]

print("Subtopics   :", len(subtopics))
print("MicroTopics :", len(microtopics))

if (len(topics), len(subtopics), len(microtopics)) != (22, 50, 105):
    errors.append("Baseline taxonomy count mismatch.")

# ---------------------------------------------------------------------
# Verify candidate presence
# ---------------------------------------------------------------------

print("\n[2] CANDIDATE PRESENCE")

for c in CANDIDATES:
    result = find_micro(c["micro_id"])

    if not result:
        print(f"{c['micro_id']:15} PRESENT: NO")
        errors.append(f"Missing candidate: {c['micro_id']}")
        continue

    actual = result["micro"].get("folder")

    print(f"{c['micro_id']:15} PRESENT: YES")
    print(f"  Label       : {c['label']}")
    print(f"  Current     : {actual}")
    print(f"  Review      : {c['question']}")

# ---------------------------------------------------------------------
# Exact decisions already established by previous academic verification
# ---------------------------------------------------------------------

print("\n[3] PREVIOUSLY VERIFIED DECISIONS")

DECISIONS = {
    "ST14_02_M02": "KEEP — corrected to explicit standard Brihattrayi works",
    "ST14_02_M03": "KEEP — corrected to standard Laghutrayi works",
    "ST02_01_M02": "KEEP — 42 Pratyahara is retained",
    "ST07_01_M01": "KEEP — Five Lakaras retained",
}

for micro_id, decision in DECISIONS.items():
    result = find_micro(micro_id)

    if result:
        print(f"{micro_id:15}: {decision}")
    else:
        errors.append(f"Previously verified node missing: {micro_id}")

# ---------------------------------------------------------------------
# Check obvious taxonomy-risk wording without changing it
# ---------------------------------------------------------------------

print("\n[4] WORDING RISK SCAN")

RISK_PATTERNS = [
    r"Seven_Masterpieces",
    r"Bhandarkar",
    r"Dyslexia",
    r"Dysgraphia",
    r"Simple_Standard_Sanskrit_Medium",
    r"NCF_FS_NCF_SE",
    r"Panchakosha",
    r"Indian_Knowledge_Systems",
]

for pattern in RISK_PATTERNS:
    matches = []

    for topic in topics:
        if re.search(pattern, json.dumps(topic, ensure_ascii=False)):
            matches.append(topic.get("id"))

    print(f"{pattern:35} topics={matches}")

# ---------------------------------------------------------------------
# Generator ↔ manifest candidate consistency
# ---------------------------------------------------------------------

print("\n[5] GENERATOR ↔ MANIFEST CANDIDATE CHECK")

for c in CANDIDATES:
    suffix = c["current"]

    manifest_hits = MANIFEST.read_text(
        encoding="utf-8"
    ).count(suffix)

    generator_hits = generator.count(suffix)

    print(
        f"{c['micro_id']:15} "
        f"generator={generator_hits} "
        f"manifest={manifest_hits}"
    )

    if manifest_hits != 1:
        errors.append(
            f"Manifest candidate count != 1: {c['micro_id']}"
        )

    # Generator contains taxonomy suffixes, not MicroTopic_ folder prefixes.
    if generator_hits != 1:
        errors.append(
            f"Generator candidate count != 1: {c['micro_id']}"
        )

# ---------------------------------------------------------------------
# Structural safety
# ---------------------------------------------------------------------

print("\n[6] STRUCTURAL SAFETY")

micro_dirs = list(
    ROOT.glob("Topic_*/Subtopic_*/MicroTopic_*")
)

legacy_dirs = list(
    ROOT.glob("Topic_*/Subtopic_*/Micro_*")
)

print("MicroTopic directories :", len(micro_dirs))
print("Legacy Micro_*         :", len(legacy_dirs))

if len(micro_dirs) != 105:
    errors.append("MicroTopic directory count changed.")

if legacy_dirs:
    errors.append("Legacy Micro_* directories detected.")

# ---------------------------------------------------------------------
# Final
# ---------------------------------------------------------------------

print("\n" + "=" * 80)
print("SANSKRIT-16 RESULT")
print("=" * 80)

if errors:
    print("FAIL")
    print(f"Total errors: {len(errors)}")
    for e in errors:
        print(" -", e)
    print("\nNO FILES WERE MODIFIED.")
    raise SystemExit(1)

print("PASS")
print()
print("All academic review candidates are present.")
print("Previously verified decisions remain intact.")
print("Generator and manifest remain synchronized.")
print("Structural tree remains intact.")
print("No files were modified.")

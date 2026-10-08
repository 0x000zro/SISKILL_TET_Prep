from pathlib import Path
import json
import re

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
MANIFEST = ROOT / "manifest.json"

with MANIFEST.open("r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 78)
print("SANSKRIT-11 — ACADEMIC TAXONOMY VERIFICATION MATRIX")
print("READ-ONLY — NO FILES WILL BE MODIFIED")
print("=" * 78)

topics = data["topics"]

# ---------------------------------------------------------------------
# Candidate academic items requiring explicit review
# ---------------------------------------------------------------------
CANDIDATES = {
    "T02": [
        (
            "42 Pratyahara",
            "FortyTwo_Pratyahara_Construction_Rules",
            "KEEP",
            "Pratyahara count/usage requires source verification."
        )
    ],
    "T07": [
        (
            "Five Lakaras",
            "Lat_Lot_Lang_Vidhiling_Lrit_Structures",
            "KEEP",
            "Current corrected transliteration/name should be retained unless "
            "authoritative syllabus requires another convention."
        )
    ],
    "T14": [
        (
            "Brihattrayi",
            "Brihattrayi_Bharavi_Magha_Sriharsha",
            "CORRECT",
            "Name should identify the three works, not only the three authors."
        ),
        (
            "Laghutrayi",
            "Laghuttrayi_Raghuvamsham_Kumarasambhavam_Megha",
            "CORRECT",
            "Canonical label/spelling and the complete third work should be explicit."
        ),
        (
            "Kalidasa major works",
            "Kalidasa_Seven_Masterpieces_Shakuntalam",
            "REVIEW_LATER",
            "Potentially ambiguous/over-specific; determine exam relevance before mutation."
        ),
    ],
    "T17": [
        (
            "Bhandarkar method",
            "Grammar_Translation_Method_Bhandarkar_Vidhi",
            "REVIEW_LATER",
            "Terminology requires authoritative academic verification."
        )
    ],
    "T18": [
        (
            "Dyslexia",
            "Reading_Comprehension_and_Dyslexia_Remediation",
            "REVIEW_LATER",
            "Verify whether this belongs in the target CTET/UPTET Sanskrit pedagogy scope."
        ),
        (
            "Dysgraphia",
            "Creative_Writing_Orthography_Dysgraphia",
            "REVIEW_LATER",
            "Verify whether this belongs in the target CTET/UPTET Sanskrit pedagogy scope."
        )
    ],
    "T22": [
        (
            "NEP/NCF terminology",
            "NEP_2020_Simple_Standard_Sanskrit_Medium",
            "REVIEW_LATER",
            "Exact policy wording and scope require authoritative verification."
        ),
        (
            "NCF/Indian Knowledge Systems",
            "NCF_FS_NCF_SE_Panchakosha_Indian_Knowledge_Systems",
            "REVIEW_LATER",
            "Verify exact NCF terminology and exam relevance."
        )
    ],
}

# ---------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------
def find_micro(topic_id, folder_name):
    for topic in topics:
        if topic["id"] != topic_id:
            continue
        for st in topic.get("subtopics", []):
            for micro in st.get("micro_topics", []):
                if micro.get("folder", "").endswith(folder_name):
                    return {
                        "topic_code": topic.get("code"),
                        "topic_name": topic.get("name_hi"),
                        "subtopic_id": st.get("id"),
                        "micro_id": micro.get("micro_id"),
                        "folder": micro.get("folder"),
                    }
    return None

# ---------------------------------------------------------------------
# General structural facts
# ---------------------------------------------------------------------
topic_ids = [t["id"] for t in topics]
subtopics = [st for t in topics for st in t.get("subtopics", [])]
micros = [m for st in subtopics for m in st.get("micro_topics", [])]

print("\n[BASELINE]")
print(f"Topics      : {len(topics)}")
print(f"Subtopics   : {len(subtopics)}")
print(f"MicroTopics : {len(micros)}")

# ---------------------------------------------------------------------
# Candidate matrix
# ---------------------------------------------------------------------
print("\n" + "=" * 78)
print("ACADEMIC VERIFICATION MATRIX")
print("=" * 78)

matrix_rows = []

for topic_id, items in CANDIDATES.items():
    for label, folder, preliminary, reason in items:
        found = find_micro(topic_id, folder)

        if found:
            state = "PRESENT"
            location = (
                f'{found["micro_id"]} | '
                f'{found["folder"]}'
            )
        else:
            state = "NOT_FOUND"
            location = "-"

        matrix_rows.append(
            (topic_id, label, preliminary, state, location, reason)
        )

for i, row in enumerate(matrix_rows, 1):
    topic_id, label, preliminary, state, location, reason = row

    print(f"\n[{i}] {topic_id} — {label}")
    print(f"    Current decision : {preliminary}")
    print(f"    Manifest state   : {state}")
    print(f"    Location         : {location}")
    print(f"    Reason           : {reason}")

# ---------------------------------------------------------------------
# Specific T14 exact taxonomy check
# ---------------------------------------------------------------------
print("\n" + "=" * 78)
print("T14 — LITERATURE PRECISION CHECK")
print("=" * 78)

t14 = next((t for t in topics if t["id"] == "T14"), None)

if not t14:
    print("T14 NOT FOUND")
else:
    for st in t14.get("subtopics", []):
        for m in st.get("micro_topics", []):
            print(
                f'{m["micro_id"]}: {m["folder"]}'
            )

# ---------------------------------------------------------------------
# Scope naming check
# ---------------------------------------------------------------------
print("\n" + "=" * 78)
print("EXAM-SCOPE LABEL CHECK")
print("=" * 78)

scope_tokens = ("UPTET", "CTET", "PAPER2", "Paper2", "PAPER_2", "Paper_2")

scope_hits = []

for t in topics:
    if any(token.lower() in t.get("code", "").lower()
           for token in scope_tokens):
        scope_hits.append(("TOPIC", t["id"], t["code"]))

    for st in t.get("subtopics", []):
        if any(token.lower() in st.get("code", "").lower()
               for token in scope_tokens):
            scope_hits.append(("SUBTOPIC", st["id"], st["code"]))

        for m in st.get("micro_topics", []):
            folder = m.get("folder", "")
            if any(token.lower() in folder.lower()
                   for token in scope_tokens):
                scope_hits.append(("MICRO", m["micro_id"], folder))

print(f"Scope-labelled taxonomy nodes: {len(scope_hits)}")

for kind, node_id, value in scope_hits:
    print(f"  {kind:8} {node_id:12} {value}")

print("\n" + "=" * 78)
print("SANSKRIT-11 RESULT")
print("=" * 78)

print("PASS — READ-ONLY ACADEMIC REVIEW MATRIX GENERATED")
print()
print("IMPORTANT:")
print("1. No files were modified.")
print("2. No folder was renamed.")
print("3. No manifest was rewritten.")
print("4. No content was generated.")
print("5. Candidate CORRECT items require a separate controlled mutation step.")
print("6. REVIEW_LATER items must not be changed merely from this audit.")
print()
print("NEXT GATE:")
print("Do not proceed to mutation until the academic decisions are explicitly")
print("reviewed and approved.")

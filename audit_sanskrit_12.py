from pathlib import Path
import json

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
MANIFEST = ROOT / "manifest.json"

with MANIFEST.open("r", encoding="utf-8") as f:
    data = json.load(f)

topics = data["topics"]

print("=" * 80)
print("SANSKRIT-12 — AUTHORITATIVE ACADEMIC DECISION MATRIX")
print("READ-ONLY — NO FILES WILL BE MODIFIED")
print("=" * 80)

DECISIONS = [
    {
        "id": "T02-ST02_01-M02",
        "current": "FortyTwo_Pratyahara_Construction_Rules",
        "decision": "KEEP",
        "canonical": "FortyTwo_Pratyahara_Construction_Rules",
        "reason": (
            "The 42-pratyahara formulation is academically defensible. "
            "Do not rename merely for stylistic reasons."
        ),
    },
    {
        "id": "T07-ST07_01-M01",
        "current": "Lat_Lot_Lang_Vidhiling_Lrit_Structures",
        "decision": "KEEP",
        "canonical": "Lat_Lot_Lang_Vidhiling_Lrit_Structures",
        "reason": (
            "The previous corruption was corrected. Lrit is retained as "
            "an ASCII transliteration label; no active corruption remains."
        ),
    },
    {
        "id": "T14-ST14_02-M02",
        "current": "Brihattrayi_Bharavi_Magha_Sriharsha",
        "decision": "CORRECT",
        "canonical": (
            "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita"
        ),
        "reason": (
            "The canonical educational label should identify the three "
            "works constituting the Brihattrayi rather than only their authors."
        ),
    },
    {
        "id": "T14-ST14_02-M03",
        "current": "Laghuttrayi_Raghuvamsham_Kumarasambhavam_Megha",
        "decision": "CORRECT",
        "canonical": (
            "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta"
        ),
        "reason": (
            "Use the standard Laghutrayi label and explicitly identify "
            "Meghaduta rather than the ambiguous abbreviation Megha."
        ),
    },
    {
        "id": "T14-ST14_02-M01",
        "current": "Kalidasa_Seven_Masterpieces_Shakuntalam",
        "decision": "REVIEW_LATER",
        "canonical": None,
        "reason": (
            "Do not change until the exact exam-oriented scope of this "
            "microtopic is separately verified."
        ),
    },
    {
        "id": "T17-ST17_01-M02",
        "current": "Grammar_Translation_Method_Bhandarkar_Vidhi",
        "decision": "REVIEW_LATER",
        "canonical": None,
        "reason": (
            "Bhandarkar/Vidhi terminology requires a dedicated academic "
            "source check before any taxonomy mutation."
        ),
    },
    {
        "id": "T18-ST18_02-M02",
        "current": "Reading_Comprehension_and_Dyslexia_Remediation",
        "decision": "REVIEW_LATER",
        "canonical": None,
        "reason": (
            "The concept may be pedagogically relevant, but its exact "
            "Sanskrit CTET/UPTET scope must be established first."
        ),
    },
    {
        "id": "T18-ST18_03-M02",
        "current": "Creative_Writing_Orthography_Dysgraphia",
        "decision": "REVIEW_LATER",
        "canonical": None,
        "reason": (
            "Scope must be verified before adding a specialised learning "
            "difficulty to the canonical Sanskrit taxonomy."
        ),
    },
    {
        "id": "T22-ST22_02-M01",
        "current": "NEP_2020_Simple_Standard_Sanskrit_Medium",
        "decision": "REVIEW_LATER",
        "canonical": None,
        "reason": (
            "Policy terminology should match authoritative NEP/NCF wording "
            "rather than an inferred taxonomy label."
        ),
    },
    {
        "id": "T22-ST22_02-M02",
        "current": "NCF_FS_NCF_SE_Panchakosha_Indian_Knowledge_Systems",
        "decision": "REVIEW_LATER",
        "canonical": None,
        "reason": (
            "Exact NCF terminology, document scope and exam relevance "
            "require separate verification."
        ),
    },
]

# ------------------------------------------------------------
# Locate every candidate in the active manifest
# ------------------------------------------------------------
def locate(folder_suffix):
    for topic in topics:
        for subtopic in topic.get("subtopics", []):
            for micro in subtopic.get("micro_topics", []):
                actual = micro.get("folder", "")
                if actual == folder_suffix or actual.endswith("_" + folder_suffix):
                    return (
                        topic["id"],
                        subtopic["id"],
                        micro["micro_id"],
                        actual,
                    )
    return None

print("\nDECISION TABLE")
print("-" * 80)

errors = 0

for item in DECISIONS:
    found = locate(item["current"])

    print(f"\n{item['id']}")
    print(f"  Current   : {item['current']}")
    print(f"  Decision  : {item['decision']}")
    print(f"  Canonical : {item['canonical'] or '(not approved for mutation)'}")
    print(f"  Present   : {'YES' if found else 'NO'}")
    print(f"  Reason    : {item['reason']}")

    if not found:
        errors += 1

# ------------------------------------------------------------
# Verify no duplicate canonical targets
# ------------------------------------------------------------
approved_targets = [
    x["canonical"]
    for x in DECISIONS
    if x["decision"] == "CORRECT" and x["canonical"]
]

duplicates = sorted(
    {x for x in approved_targets if approved_targets.count(x) > 1}
)

print("\n" + "=" * 80)
print("CANONICAL TARGET CHECK")
print("=" * 80)
print(f"Approved correction targets : {len(approved_targets)}")
print(f"Duplicate targets           : {len(duplicates)}")

for d in duplicates:
    print("  DUPLICATE:", d)

# ------------------------------------------------------------
# Confirm active tree remains untouched
# ------------------------------------------------------------
print("\n" + "=" * 80)
print("ACTIVE TREE SAFETY CHECK")
print("=" * 80)

legacy_micro = list(ROOT.glob("Topic_*/*/Micro_*"))
canonical_micro = list(ROOT.glob("Topic_*/*/MicroTopic_*"))

print(f"Legacy Micro_* directories     : {len(legacy_micro)}")
print(f"Canonical MicroTopic_* dirs    : {len(canonical_micro)}")

print("\n" + "=" * 80)
print("SANSKRIT-12 RESULT")
print("=" * 80)

if errors == 0 and not duplicates and len(canonical_micro) == 105:
    print("PASS")
    print()
    print("Academic decision matrix is internally consistent.")
    print("Two T14 corrections are approved candidates:")
    print("  1. Brihattrayi -> explicit three works")
    print("  2. Laghutrayi -> standard label + Meghaduta")
    print()
    print("IMPORTANT:")
    print("This script is READ-ONLY.")
    print("No generator, manifest, folder, or content file was modified.")
else:
    print("FAIL")
    print(f"Location errors : {errors}")
    print(f"Duplicate targets : {len(duplicates)}")

print("\nNEXT GATE:")
print("Do not perform mutation from this script.")
print("Mutation requires a separate controlled SANSKRIT-13 step.")

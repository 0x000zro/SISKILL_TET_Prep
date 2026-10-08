from pathlib import Path
import json

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
GEN = Path("build_sanskrit_framework.py")
MANIFEST = ROOT / "manifest.json"

print("=" * 72)
print("SANSKRIT-18 — CONTROLLED TAXONOMY CORRECTION DRY-RUN")
print("=" * 72)

with open(MANIFEST, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(GEN, "r", encoding="utf-8") as f:
    generator = f.read()

# Academic candidates approved for controlled taxonomy review.
# DRY-RUN ONLY: no files or directories are modified.
changes = [
    (
        "ST14_02_M01",
        "MicroTopic_01_Kalidasa_Seven_Masterpieces_Shakuntalam",
        "MicroTopic_01_Kalidasa_Seven_Major_Works",
    ),
    (
        "ST17_01_M02",
        "MicroTopic_02_Grammar_Translation_Method_Bhandarkar_Vidhi",
        "MicroTopic_02_Grammar_Translation_Method_and_Bhandarkar_Method",
    ),
    (
        "ST18_03_M01",
        "MicroTopic_01_Calligraphy_Transcription_Dictation_Sulekha",
        "MicroTopic_01_Writing_Skills_Calligraphy_Transcription_Dictation",
    ),
    (
        "ST22_01_M01",
        "MicroTopic_01_Eighth_Schedule_Classical_Language_Status",
        "MicroTopic_01_Eighth_Schedule_and_Classical_Language_Status",
    ),
    (
        "ST22_01_M02",
        "MicroTopic_02_Three_Language_Formula_Kothari_Commission",
        "MicroTopic_02_Three_Language_Formula_and_Kothari_Commission",
    ),
    (
        "ST22_02_M01",
        "MicroTopic_01_NEP_2020_Simple_Standard_Sanskrit_Medium",
        "MicroTopic_01_NEP_2020_and_Simple_Standard_Sanskrit",
    ),
    (
        "ST22_02_M02",
        "MicroTopic_02_NCF_FS_NCF_SE_Panchakosha_Indian_Knowledge_Systems",
        "MicroTopic_02_NCF_FS_NCF_SE_and_Indian_Knowledge_Systems",
    ),
]

# ---------------------------------------------------------------------
# Build manifest index using the ACTUAL canonical manifest contract.
# ---------------------------------------------------------------------

micros = {}

for topic in data["topics"]:
    for subtopic in topic["subtopics"]:
        for micro in subtopic["micro_topics"]:
            micro_id = micro["micro_id"]
            micros[micro_id] = micro

errors = 0

# ---------------------------------------------------------------------
# 1. Baseline
# ---------------------------------------------------------------------

print("\n[1] BASELINE")
print("-" * 72)

print("Topics       :", data["total_topics"])
print("Subtopics    :", data["total_subtopics"])
print("MicroTopics  :", data["total_microtopics"])
print("Status       :", data["status"])

if data["total_topics"] != 22:
    print("ERROR: expected 22 topics")
    errors += 1

if data["total_subtopics"] != 50:
    print("ERROR: expected 50 subtopics")
    errors += 1

if data["total_microtopics"] != 105:
    print("ERROR: expected 105 microtopics")
    errors += 1

if data["status"] != "scaffolded":
    print("ERROR: expected status=scaffolded")
    errors += 1

# ---------------------------------------------------------------------
# 2. Proposed taxonomy changes
# ---------------------------------------------------------------------

print("\n[2] PROPOSED CHANGES — DRY RUN ONLY")
print("-" * 72)

for micro_id, old_name, new_name in changes:

    print(f"\n{micro_id}")
    print("  OLD:", old_name)
    print("  NEW:", new_name)

    micro = micros.get(micro_id)

    if micro is None:
        print("  Manifest micro_id: FAIL — ID not found")
        errors += 1
        continue

    actual_folder = micro.get("folder", "")

    if actual_folder != old_name:
        print("  Manifest current folder: FAIL")
        print("  Actual:", actual_folder)
        errors += 1
    else:
        print("  Manifest current folder: PASS")

    # Generator references
    old_gen = generator.count(old_name)
    new_gen = generator.count(new_name)

    if old_gen != 1:
        print(f"  Generator OLD reference: FAIL ({old_gen})")
        errors += 1
    else:
        print("  Generator OLD reference: PASS (1)")

    if new_gen != 0:
        print(f"  Generator NEW reference already exists: FAIL ({new_gen})")
        errors += 1
    else:
        print("  Generator NEW reference: PASS (0)")

    # Physical directories
    old_dirs = [
        p for p in ROOT.rglob(old_name)
        if p.is_dir()
    ]

    new_dirs = [
        p for p in ROOT.rglob(new_name)
        if p.is_dir()
    ]

    if len(old_dirs) != 1:
        print(f"  Physical OLD directory: FAIL ({len(old_dirs)})")
        errors += 1
    else:
        print("  Physical OLD directory: PASS (1)")

    if len(new_dirs) != 0:
        print(
            f"  Physical NEW directory already exists: FAIL ({len(new_dirs)})"
        )
        errors += 1
    else:
        print("  Physical NEW directory: PASS (0)")

# ---------------------------------------------------------------------
# 3. Global invariants
# ---------------------------------------------------------------------

print("\n[3] GLOBAL INVARIANTS")
print("-" * 72)

all_micro_ids = []

for topic in data["topics"]:
    for subtopic in topic["subtopics"]:
        for micro in subtopic["micro_topics"]:
            all_micro_ids.append(micro["micro_id"])

duplicates = sorted({
    x for x in all_micro_ids
    if all_micro_ids.count(x) > 1
})

if duplicates:
    print("Duplicate micro IDs: FAIL")
    for x in duplicates:
        print(" ", x)
    errors += 1
else:
    print("Duplicate micro IDs: PASS (0)")

canonical_dirs = [
    p for p in ROOT.rglob("MicroTopic_*")
    if p.is_dir()
]

legacy_dirs = [
    p for p in ROOT.rglob("Micro_*")
    if p.is_dir() and not p.name.startswith("MicroTopic_")
]

print("Canonical MicroTopic dirs:", len(canonical_dirs))
print("Legacy Micro dirs       :", len(legacy_dirs))

if len(canonical_dirs) != 105:
    print("ERROR: expected 105 canonical MicroTopic directories")
    errors += 1

if len(legacy_dirs) != 0:
    print("ERROR: legacy Micro_* directories still exist")
    errors += 1

# ---------------------------------------------------------------------
# 4. Target folder uniqueness
# ---------------------------------------------------------------------

print("\n[4] TARGET NAME SAFETY")
print("-" * 72)

target_names = [new_name for _, _, new_name in changes]

if len(target_names) != len(set(target_names)):
    print("Duplicate proposed target names: FAIL")
    errors += 1
else:
    print("Duplicate proposed target names: PASS (0)")

for name in target_names:
    matches = [
        p for p in ROOT.rglob(name)
        if p.is_dir()
    ]

    if matches:
        print(f"Target already exists: FAIL — {name}")
        errors += 1
    else:
        print(f"Target available: PASS — {name}")

# ---------------------------------------------------------------------
# 5. Safety
# ---------------------------------------------------------------------

print("\n[5] SAFETY CHECK")
print("-" * 72)

print("Files modified      : 0")
print("Directories renamed : 0")
print("Content generated   : 0")
print("Backups modified    : 0")

# ---------------------------------------------------------------------
# Final result
# ---------------------------------------------------------------------

print("\n" + "=" * 72)

if errors == 0:
    print("SANSKRIT-18 DRY-RUN PASS")
    print("No files were modified.")
    print("All proposed targets are structurally safe.")
else:
    print(f"SANSKRIT-18 DRY-RUN FAIL — {errors} issue(s)")
    print("DO NOT MODIFY ANY FILE.")

print("=" * 72)

from pathlib import Path
import json

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
GEN = Path("build_sanskrit_framework.py")
MANIFEST = ROOT / "manifest.json"

MICRO_ID = "ST22_02_M01"

OLD_BASE = "NEP_2020_Simple_Standard_Sanskrit_Medium"
NEW_BASE = "NEP_2020_and_Simple_Standard_Sanskrit"

OLD_FOLDER = "MicroTopic_01_" + OLD_BASE
NEW_FOLDER = "MicroTopic_01_" + NEW_BASE

print("=" * 72)
print("SANSKRIT-20 — SINGLE-CHANGE TAXONOMY DRY-RUN")
print("=" * 72)

with open(MANIFEST, encoding="utf-8") as f:
    manifest = json.load(f)

with open(GEN, encoding="utf-8") as f:
    generator = f.read()

errors = 0

# ------------------------------------------------------------
# 1. Baseline
# ------------------------------------------------------------

print("\n[1] BASELINE")
print("-" * 72)

print("Topics       :", manifest["total_topics"])
print("Subtopics    :", manifest["total_subtopics"])
print("MicroTopics  :", manifest["total_microtopics"])
print("Status       :", manifest["status"])

if (
    manifest["total_topics"] != 22
    or manifest["total_subtopics"] != 50
    or manifest["total_microtopics"] != 105
):
    print("FAIL: baseline totals changed")
    errors += 1
else:
    print("Baseline totals: PASS")

if manifest["status"] != "scaffolded":
    print("FAIL: status is not scaffolded")
    errors += 1
else:
    print("Status: PASS")

# ------------------------------------------------------------
# 2. Locate target
# ------------------------------------------------------------

print("\n[2] TARGET VERIFICATION")
print("-" * 72)

target = None

for topic in manifest["topics"]:
    for subtopic in topic["subtopics"]:
        for micro in subtopic["micro_topics"]:
            if micro["micro_id"] == MICRO_ID:
                target = micro

if target is None:
    print("FAIL: target micro_id not found")
    errors += 1
else:
    print("Micro ID:", MICRO_ID)
    print("Current folder:", target["folder"])

    if target["folder"] == OLD_FOLDER:
        print("Current folder: PASS")
    else:
        print("FAIL: unexpected current folder")
        errors += 1

# ------------------------------------------------------------
# 3. Generator taxonomy verification
# ------------------------------------------------------------

print("\n[3] GENERATOR TAXONOMY")
print("-" * 72)

old_count = generator.count(OLD_BASE)
new_count = generator.count(NEW_BASE)

print("OLD base-name occurrences:", old_count)
print("NEW base-name occurrences:", new_count)

if old_count != 1:
    print("FAIL: expected exactly one OLD taxonomy entry")
    errors += 1
else:
    print("OLD taxonomy entry: PASS (1)")

if new_count != 0:
    print("FAIL: NEW taxonomy entry already exists")
    errors += 1
else:
    print("NEW taxonomy entry: PASS (0)")

# ------------------------------------------------------------
# 4. Physical directory verification
# ------------------------------------------------------------

print("\n[4] PHYSICAL DIRECTORY")
print("-" * 72)

old_dirs = [
    p for p in ROOT.rglob(OLD_FOLDER)
    if p.is_dir()
]

new_dirs = [
    p for p in ROOT.rglob(NEW_FOLDER)
    if p.is_dir()
]

print("OLD directory count:", len(old_dirs))
print("NEW directory count:", len(new_dirs))

if len(old_dirs) != 1:
    print("FAIL: expected exactly one OLD directory")
    errors += 1
else:
    print("OLD directory: PASS (1)")

if len(new_dirs) != 0:
    print("FAIL: NEW directory already exists")
    errors += 1
else:
    print("NEW directory available: PASS (0)")

# ------------------------------------------------------------
# 5. Asset preservation check
# ------------------------------------------------------------

print("\n[5] ASSET PRESERVATION")
print("-" * 72)

if old_dirs:
    asset_names = [
        "Concept/content.md",
        "Short_Notes/content.md",
        "PYQ/content.json",
        "MCQ/content.json",
        "Practice/content.md",
    ]

    missing = []

    for rel in asset_names:
        if not (old_dirs[0] / rel).is_file():
            missing.append(rel)

    if missing:
        print("FAIL: missing assets:")
        for x in missing:
            print(" ", x)
        errors += 1
    else:
        print("All 5 existing assets: PASS")

# ------------------------------------------------------------
# 6. Global structural invariants
# ------------------------------------------------------------

print("\n[6] GLOBAL STRUCTURAL INVARIANTS")
print("-" * 72)

micro_ids = []

for topic in manifest["topics"]:
    for subtopic in topic["subtopics"]:
        for micro in subtopic["micro_topics"]:
            micro_ids.append(micro["micro_id"])

duplicates = sorted({
    x for x in micro_ids
    if micro_ids.count(x) > 1
})

print("Duplicate micro IDs:", len(duplicates))

if duplicates:
    for x in duplicates:
        print(" ", x)
    errors += 1
else:
    print("Duplicate IDs: PASS (0)")

canonical_dirs = [
    p for p in ROOT.rglob("MicroTopic_*")
    if p.is_dir()
]

legacy_dirs = [
    p for p in ROOT.rglob("Micro_*")
    if p.is_dir() and not p.name.startswith("MicroTopic_")
]

print("Canonical MicroTopic dirs:", len(canonical_dirs))
print("Legacy Micro dirs:", len(legacy_dirs))

if len(canonical_dirs) != 105:
    print("FAIL: canonical MicroTopic count is not 105")
    errors += 1

if legacy_dirs:
    print("FAIL: legacy Micro_* directories exist")
    errors += 1

# ------------------------------------------------------------
# 7. Safety
# ------------------------------------------------------------

print("\n[7] SAFETY")
print("-" * 72)

print("Files modified      : 0")
print("Directories renamed : 0")
print("Content generated   : 0")
print("Backups modified    : 0")

# ------------------------------------------------------------
# Final
# ------------------------------------------------------------

print("\n" + "=" * 72)

if errors == 0:
    print("SANSKRIT-20 DRY-RUN PASS")
    print("Exactly ONE taxonomy rename is proposed.")
    print("No files were modified.")
else:
    print(f"SANSKRIT-20 DRY-RUN FAIL — {errors} issue(s)")
    print("DO NOT MODIFY ANY FILE.")

print("=" * 72)

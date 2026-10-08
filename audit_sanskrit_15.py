from pathlib import Path
import json
import hashlib
import sys

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
MANIFEST = ROOT / "manifest.json"
MASTER = Path("UPTET_CTET/Paper_1_and_2/master_manifest.json")
GENERATOR = Path("build_sanskrit_framework.py")

EXPECTED_ASSETS = [
    "Concept",
    "Short_Notes",
    "PYQ",
    "MCQ",
    "Practice",
]

EXPECTED_T14 = {
    "ST14_02_M02":
        "MicroTopic_02_Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita",
    "ST14_02_M03":
        "MicroTopic_03_Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta",
}

OLD_NAMES = [
    "Brihattrayi_Bharavi_Magha_Sriharsha",
    "Laghuttrayi_Raghuvamsham_Kumarasambhavam_Megha",
]

print("=" * 80)
print("SANSKRIT-15 — INDEPENDENT POST-MUTATION STRUCTURAL VERIFICATION")
print("READ-ONLY — NO FILES WILL BE MODIFIED")
print("=" * 80)

errors = []

# ---------------------------------------------------------------------
# Load manifests
# ---------------------------------------------------------------------
try:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
except Exception as e:
    raise SystemExit(f"FAIL: Cannot read Sanskrit manifest: {e}")

try:
    master = json.loads(MASTER.read_text(encoding="utf-8"))
except Exception as e:
    raise SystemExit(f"FAIL: Cannot read master manifest: {e}")

generator_text = GENERATOR.read_text(encoding="utf-8")

# ---------------------------------------------------------------------
# 1. Canonical manifest
# ---------------------------------------------------------------------
print("\n[1] CANONICAL MANIFEST")

required_keys = [
    "schema_version",
    "framework_version",
    "content_version",
    "taxonomy_version",
    "status",
    "exam_scope",
    "paper_scope",
    "subject",
    "total_topics",
    "total_subtopics",
    "total_microtopics",
    "asset_types",
    "topics",
]

for key in required_keys:
    if key not in manifest:
        errors.append(f"Missing manifest key: {key}")

print("schema_version   :", manifest.get("schema_version"))
print("framework_version:", manifest.get("framework_version"))
print("content_version  :", manifest.get("content_version"))
print("taxonomy_version :", manifest.get("taxonomy_version"))
print("status           :", manifest.get("status"))

if manifest.get("status") != "scaffolded":
    errors.append("Sanskrit status is not scaffolded.")

# ---------------------------------------------------------------------
# 2. Subject
# ---------------------------------------------------------------------
print("\n[2] SUBJECT")

subject = manifest.get("subject", {})

print("id      :", subject.get("id"))
print("name_en :", subject.get("name_en"))
print("name_hi :", subject.get("name_hi"))
print("type    :", subject.get("type"))

if subject.get("id") != "SAN":
    errors.append("Subject ID != SAN")

if subject.get("name_en") != "Sanskrit Language and Pedagogy":
    errors.append("Incorrect Sanskrit English name")

if subject.get("name_hi") != "संस्कृत भाषा एवं शिक्षण शास्त्र":
    errors.append("Incorrect Sanskrit Hindi name")

if subject.get("type") != "language_pedagogy":
    errors.append("Incorrect Sanskrit subject type")

# ---------------------------------------------------------------------
# 3. Taxonomy counts and IDs
# ---------------------------------------------------------------------
topics = manifest.get("topics", [])

subtopics = [
    st
    for t in topics
    for st in t.get("subtopics", [])
]

micros = [
    m
    for st in subtopics
    for m in st.get("micro_topics", [])
]

print("\n[3] TAXONOMY")

print("Topics      :", len(topics))
print("Subtopics   :", len(subtopics))
print("MicroTopics :", len(micros))

if len(topics) != 22:
    errors.append(f"Expected 22 topics, found {len(topics)}")

if len(subtopics) != 50:
    errors.append(f"Expected 50 subtopics, found {len(subtopics)}")

if len(micros) != 105:
    errors.append(f"Expected 105 microtopics, found {len(micros)}")

topic_ids = [t.get("id") for t in topics]
subtopic_ids = [s.get("id") for s in subtopics]
micro_ids = [m.get("micro_id") for m in micros]

print("Duplicate topic IDs     :", len(topic_ids) - len(set(topic_ids)))
print("Duplicate subtopic IDs  :", len(subtopic_ids) - len(set(subtopic_ids)))
print("Duplicate micro IDs     :", len(micro_ids) - len(set(micro_ids)))

if len(topic_ids) != len(set(topic_ids)):
    errors.append("Duplicate topic IDs")

if len(subtopic_ids) != len(set(subtopic_ids)):
    errors.append("Duplicate subtopic IDs")

if len(micro_ids) != len(set(micro_ids)):
    errors.append("Duplicate micro IDs")

# ---------------------------------------------------------------------
# 4. Manifest totals
# ---------------------------------------------------------------------
print("\n[4] MANIFEST TOTALS")

totals = {
    "total_topics": len(topics),
    "total_subtopics": len(subtopics),
    "total_microtopics": len(micros),
}

for key, actual in totals.items():
    declared = manifest.get(key)
    print(f"{key:20}: declared={declared} actual={actual}")

    if declared != actual:
        errors.append(
            f"Manifest total mismatch: {key}: {declared} != {actual}"
        )

# ---------------------------------------------------------------------
# 5. Asset types
# ---------------------------------------------------------------------
print("\n[5] ASSET TYPES")

print("Manifest assets:", manifest.get("asset_types"))

if manifest.get("asset_types") != EXPECTED_ASSETS:
    errors.append("Asset type list does not match canonical contract.")

# ---------------------------------------------------------------------
# 6. Physical tree
# ---------------------------------------------------------------------
print("\n[6] PHYSICAL TREE")

topic_dirs = list(ROOT.glob("Topic_*"))
subtopic_dirs = list(ROOT.glob("Topic_*/Subtopic_*"))
micro_dirs = list(ROOT.glob("Topic_*/Subtopic_*/MicroTopic_*"))
legacy_dirs = list(ROOT.glob("Topic_*/Subtopic_*/Micro_*"))

print("Topic directories       :", len(topic_dirs))
print("Subtopic directories    :", len(subtopic_dirs))
print("MicroTopic directories  :", len(micro_dirs))
print("Legacy Micro directories:", len(legacy_dirs))

if len(topic_dirs) != 22:
    errors.append("Physical topic directory count != 22")

if len(subtopic_dirs) != 50:
    errors.append("Physical subtopic directory count != 50")

if len(micro_dirs) != 105:
    errors.append("Physical MicroTopic directory count != 105")

if legacy_dirs:
    errors.append("Legacy Micro_* directories still exist")

# ---------------------------------------------------------------------
# 7. Asset completeness
# ---------------------------------------------------------------------
print("\n[7] ASSET COMPLETENESS")

asset_counts = {}

for asset in EXPECTED_ASSETS:
    count = len(
        list(
            ROOT.glob(
                f"Topic_*/Subtopic_*/MicroTopic_*/{asset}/*"
            )
        )
    )

    asset_counts[asset] = count

    print(f"{asset:12}: {count}")

    if count != 105:
        errors.append(
            f"{asset} asset count != 105"
        )

total_assets = sum(asset_counts.values())

print("TOTAL ASSETS :", total_assets)

if total_assets != 525:
    errors.append(
        f"Expected 525 total asset files, found {total_assets}"
    )

# ---------------------------------------------------------------------
# 8. Asset structural completeness
# ---------------------------------------------------------------------
print("\n[8] ASSET STRUCTURE")

missing_assets = []
unexpected_files = []

for micro in micro_dirs:
    for asset in EXPECTED_ASSETS:
        asset_dir = micro / asset

        if not asset_dir.exists():
            missing_assets.append(str(asset_dir))
            continue

        files = [p for p in asset_dir.iterdir() if p.is_file()]

        if len(files) != 1:
            unexpected_files.append(
                f"{asset_dir} -> {len(files)} files"
            )

print("Missing asset structures :", len(missing_assets))
print("Invalid asset structures :", len(unexpected_files))

if missing_assets:
    errors.extend(
        f"Missing asset: {x}" for x in missing_assets
    )

if unexpected_files:
    errors.extend(
        f"Invalid asset structure: {x}" for x in unexpected_files
    )

# ---------------------------------------------------------------------
# 9. T14 exact verification
# ---------------------------------------------------------------------
print("\n[9] T14 POST-MUTATION VERIFICATION")

t14 = next((t for t in topics if t.get("id") == "T14"), None)

if not t14:
    errors.append("T14 missing")
else:
    t14_micros = [
        m
        for st in t14.get("subtopics", [])
        for m in st.get("micro_topics", [])
    ]

    print("T14 MicroTopics:", len(t14_micros))

    by_id = {
        m.get("micro_id"): m
        for m in t14_micros
    }

    for micro_id, expected_folder in EXPECTED_T14.items():

        if micro_id not in by_id:
            errors.append(f"T14 missing Micro ID: {micro_id}")
            continue

        actual = by_id[micro_id].get("folder")

        print(f"\n{micro_id}")
        print("Expected:", expected_folder)
        print("Actual  :", actual)

        if actual != expected_folder:
            errors.append(
                f"{micro_id} folder mismatch"
            )

# ---------------------------------------------------------------------
# 10. Old names must be absent
# ---------------------------------------------------------------------
print("\n[10] OLD TAXONOMY TOKEN SCAN")

for old in OLD_NAMES:

    generator_hits = generator_text.count(old)
    manifest_hits = MANIFEST.read_text(
        encoding="utf-8"
    ).count(old)

    physical_hits = len(
        list(ROOT.glob(f"**/*{old}*"))
    )

    print(f"\n{old}")
    print("Generator :", generator_hits)
    print("Manifest  :", manifest_hits)
    print("Physical  :", physical_hits)

    if generator_hits != 0:
        errors.append(f"Old generator token remains: {old}")

    if manifest_hits != 0:
        errors.append(f"Old manifest token remains: {old}")

    if physical_hits != 0:
        errors.append(f"Old physical token remains: {old}")

# ---------------------------------------------------------------------
# 11. New names exactly once in generator/manifest
# ---------------------------------------------------------------------
print("\n[11] NEW TAXONOMY TOKEN CHECK")

NEW_GENERATOR_SUFFIXES = [
    "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita",
    "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta",
]

manifest_text = MANIFEST.read_text(encoding="utf-8")

for suffix in NEW_GENERATOR_SUFFIXES:

    generator_hits = generator_text.count(suffix)
    manifest_hits = manifest_text.count(suffix)

    print(f"\n{suffix}")
    print("Generator :", generator_hits)
    print("Manifest  :", manifest_hits)

    if generator_hits != 1:
        errors.append(
            f"New generator taxonomy suffix count != 1: {suffix}"
        )

    if manifest_hits != 1:
        errors.append(
            f"New manifest taxonomy suffix count != 1: {suffix}"
        )

# ---------------------------------------------------------------------
# 12. Generator / manifest T14 consistency
# ---------------------------------------------------------------------
print("\n[12] GENERATOR ↔ MANIFEST CONSISTENCY")

for old, new in {
    "Brihattrayi_Bharavi_Magha_Sriharsha":
        "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita",
    "Laghuttrayi_Raghuvamsham_Kumarasambhavam_Megha":
        "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta",
}.items():

    g = generator_text.count(new)
    m = MANIFEST.read_text(encoding="utf-8").count(new)

    print(f"{new}")
    print(f"  generator={g}, manifest={m}")

    if g != m:
        errors.append(
            f"Generator/manifest mismatch: {new}"
        )

# ---------------------------------------------------------------------
# 13. Master manifest
# ---------------------------------------------------------------------
print("\n[13] MASTER MANIFEST")

san_entries = [
    x
    for x in master.get("subjects", [])
    if x.get("id") == "SAN"
]

print("SAN entries:", len(san_entries))

if len(san_entries) != 1:
    errors.append(
        f"Expected exactly one SAN master entry, found {len(san_entries)}"
    )
else:
    san = san_entries[0]

    checks = {
        "name_en": "Sanskrit Language and Pedagogy",
        "name_hi": "संस्कृत भाषा एवं शिक्षण शास्त्र",
        "directory": "Sanskrit",
        "manifest_path":
            "Sanskrit/manifest.json",
        "status": "scaffolded",
        "total_topics": 22,
        "framework_version": "1.0.0",
        "taxonomy_version": "1.0.0",
    }

    for key, expected in checks.items():
        actual = san.get(key)

        print(f"{key:20}: {actual}")

        if actual != expected:
            errors.append(
                f"Master SAN mismatch: {key}: "
                f"{actual!r} != {expected!r}"
            )

print(
    "active_subjects_count :",
    master.get("active_subjects_count")
)

print(
    "total_planned_subjects:",
    master.get("total_planned_subjects")
)

if master.get("active_subjects_count") != 6:
    errors.append("Master active_subjects_count != 6")

if master.get("total_planned_subjects") != 6:
    errors.append("Master total_planned_subjects != 6")

# ---------------------------------------------------------------------
# 14. Backup presence
# ---------------------------------------------------------------------
print("\n[14] BACKUP PRESENCE")

generator_backups = list(
    Path(".").glob("build_sanskrit_framework.py.backup*")
)

manifest_backups = list(
    ROOT.glob("manifest.json.backup*")
)

print("Generator backups:", len(generator_backups))
print("Manifest backups :", len(manifest_backups))

if not generator_backups:
    errors.append("No Sanskrit generator backup found")

if not manifest_backups:
    errors.append("No Sanskrit manifest backup found")

for p in generator_backups:
    print(" ", p)

for p in manifest_backups:
    print(" ", p)

# ---------------------------------------------------------------------
# 15. Final
# ---------------------------------------------------------------------
print("\n" + "=" * 80)
print("SANSKRIT-15 RESULT")
print("=" * 80)

if errors:
    print("FAIL")
    print(f"Total errors: {len(errors)}")
    print()

    for e in errors:
        print(" -", e)

    print("\nNO FILES WERE MODIFIED.")
    sys.exit(1)

print("PASS")
print()
print("Sanskrit post-mutation structure is internally consistent.")
print("T14 taxonomy correction is structurally synchronized.")
print("All 105 MicroTopics remain present.")
print("All 525 asset files remain present.")
print("No legacy Micro_* directories remain.")
print("MicroTopic IDs remain unchanged.")
print("Master manifest remains synchronized.")
print("No files were modified by this verification.")

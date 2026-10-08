from pathlib import Path
from datetime import datetime
import json
import hashlib
import shutil
import sys

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
MANIFEST = ROOT / "manifest.json"
GENERATOR = Path("build_sanskrit_framework.py")

CORRECTIONS = {
    "Brihattrayi_Bharavi_Magha_Sriharsha":
        "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita",

    "Laghuttrayi_Raghuvamsham_Kumarasambhavam_Megha":
        "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta",
}

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

GEN_BACKUP = Path(
    f"build_sanskrit_framework.py.backup_SANSKRIT-14_{TIMESTAMP}"
)

MANIFEST_BACKUP = ROOT / (
    f"manifest.json.backup_SANSKRIT-14_{TIMESTAMP}"
)

print("=" * 80)
print("SANSKRIT-14 — CONTROLLED T14 TAXONOMY MUTATION")
print("=" * 80)

# ---------------------------------------------------------------------
# Safety preflight
# ---------------------------------------------------------------------
if not ROOT.exists():
    raise SystemExit("FAIL: Sanskrit root directory missing.")

if not MANIFEST.exists():
    raise SystemExit("FAIL: Sanskrit manifest missing.")

if not GENERATOR.exists():
    raise SystemExit("FAIL: Sanskrit generator missing.")

with MANIFEST.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

# ---------------------------------------------------------------------
# Locate exact T14 / ST14_02 microtopics
# ---------------------------------------------------------------------
targets = {}

for topic in manifest["topics"]:
    if topic["id"] != "T14":
        continue

    for subtopic in topic.get("subtopics", []):
        if subtopic["id"] != "ST14_02":
            continue

        for micro in subtopic.get("micro_topics", []):
            folder = micro["folder"]

            for old, new in CORRECTIONS.items():
                if folder.endswith(old):
                    targets[old] = {
                        "micro_id": micro["micro_id"],
                        "old_folder": folder,
                        "new_folder": folder.replace(old, new),
                    }

if len(targets) != 2:
    raise SystemExit(
        f"FAIL: Expected 2 mutation targets, found {len(targets)}."
    )

print("\n[1] PREFLIGHT TARGETS")

for old, new in CORRECTIONS.items():
    x = targets[old]

    print(f"\nMicro ID   : {x['micro_id']}")
    print(f"OLD folder : {x['old_folder']}")
    print(f"NEW folder : {x['new_folder']}")

# ---------------------------------------------------------------------
# Resolve physical directories
# ---------------------------------------------------------------------
physical = {}

for old, new in CORRECTIONS.items():
    candidates = list(
        ROOT.glob(
            f"Topic_14_Sanskrit_Literature_Epics_Poets_UPTET/"
            f"Subtopic_02_Kalidasa_and_Brihattrayi_Laghuttrayi/"
            f"MicroTopic_*_{old}"
        )
    )

    if len(candidates) != 1:
        raise SystemExit(
            f"FAIL: Expected exactly one physical directory for {old}; "
            f"found {len(candidates)}."
        )

    old_path = candidates[0]
    new_path = old_path.parent / old_path.name.replace(old, new)

    if new_path.exists():
        raise SystemExit(
            f"FAIL: Target directory already exists: {new_path}"
        )

    physical[old] = (old_path, new_path)

# ---------------------------------------------------------------------
# Capture hashes BEFORE mutation
# ---------------------------------------------------------------------
def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

before_hashes = {}

print("\n[2] ASSET HASH BASELINE")

for old, (old_path, new_path) in physical.items():
    files = sorted(p for p in old_path.rglob("*") if p.is_file())

    print(f"\n{old}")
    print(f"  Files: {len(files)}")

    for p in files:
        rel = p.relative_to(old_path)
        before_hashes[(old, str(rel))] = sha256(p)
        print(f"  {rel} : {before_hashes[(old, str(rel))]}")

# ---------------------------------------------------------------------
# Backup source files
# ---------------------------------------------------------------------
print("\n[3] BACKUPS")

if GEN_BACKUP.exists():
    raise SystemExit(f"FAIL: Backup collision: {GEN_BACKUP}")

if MANIFEST_BACKUP.exists():
    raise SystemExit(f"FAIL: Backup collision: {MANIFEST_BACKUP}")

shutil.copy2(GENERATOR, GEN_BACKUP)
shutil.copy2(MANIFEST, MANIFEST_BACKUP)

print(f"Generator backup : {GEN_BACKUP}")
print(f"Manifest backup  : {MANIFEST_BACKUP}")

# ---------------------------------------------------------------------
# Perform physical directory rename
# ---------------------------------------------------------------------
print("\n[4] PHYSICAL DIRECTORY RENAMES")

renamed = []

try:
    for old, (old_path, new_path) in physical.items():
        old_path.rename(new_path)
        renamed.append((old, old_path, new_path))
        print(f"RENAMED:")
        print(f"  {old_path}")
        print(f"  -> {new_path}")

except Exception as e:
    print("\nPHYSICAL RENAME ERROR:", e)

    # Roll back any already-renamed directories
    for old, old_path, new_path in reversed(renamed):
        if new_path.exists() and not old_path.exists():
            new_path.rename(old_path)

    raise SystemExit("FAIL: Physical rename rolled back.")

# ---------------------------------------------------------------------
# Update generator
# ---------------------------------------------------------------------
print("\n[5] GENERATOR UPDATE")

generator_text = GENERATOR.read_text(encoding="utf-8")

for old, new in CORRECTIONS.items():
    count = generator_text.count(old)

    if count != 1:
        raise SystemExit(
            f"FAIL: Expected exactly 1 generator occurrence of {old}; "
            f"found {count}."
        )

    generator_text = generator_text.replace(old, new)

GENERATOR.write_text(generator_text, encoding="utf-8")

print("Generator updated: 2 taxonomy references.")

# ---------------------------------------------------------------------
# Update manifest
# ---------------------------------------------------------------------
print("\n[6] MANIFEST UPDATE")

manifest_text = MANIFEST.read_text(encoding="utf-8")

for old, new in CORRECTIONS.items():
    count = manifest_text.count(old)

    if count != 1:
        raise SystemExit(
            f"FAIL: Expected exactly 1 manifest occurrence of {old}; "
            f"found {count}."
        )

    manifest_text = manifest_text.replace(old, new)

MANIFEST.write_text(manifest_text, encoding="utf-8")

print("Manifest updated: 2 taxonomy references.")

# ---------------------------------------------------------------------
# Reload and validate manifest
# ---------------------------------------------------------------------
print("\n[7] POST-MUTATION VALIDATION")

with MANIFEST.open("r", encoding="utf-8") as f:
    new_manifest = json.load(f)

validated = {}

for topic in new_manifest["topics"]:
    if topic["id"] != "T14":
        continue

    for subtopic in topic.get("subtopics", []):
        if subtopic["id"] != "ST14_02":
            continue

        for micro in subtopic.get("micro_topics", []):
            folder = micro["folder"]

            for old, new in CORRECTIONS.items():
                if folder.endswith(new):
                    validated[new] = {
                        "micro_id": micro["micro_id"],
                        "folder": folder,
                    }

if len(validated) != 2:
    raise SystemExit(
        f"FAIL: Expected 2 corrected manifest entries, found {len(validated)}."
    )

for old, new in CORRECTIONS.items():
    entry = validated[new]

    print(f"\nNEW taxonomy: {new}")
    print(f"Micro ID    : {entry['micro_id']}")
    print(f"Folder      : {entry['folder']}")

# ---------------------------------------------------------------------
# Validate physical tree and hashes
# ---------------------------------------------------------------------
print("\n[8] PHYSICAL TREE + HASH VALIDATION")

for old, (old_path, new_path) in physical.items():

    if old_path.exists():
        raise SystemExit(
            f"FAIL: Old directory still exists: {old_path}"
        )

    if not new_path.exists():
        raise SystemExit(
            f"FAIL: New directory missing: {new_path}"
        )

    files_after = sorted(
        p for p in new_path.rglob("*") if p.is_file()
    )

    print(f"\n{new_path}")
    print(f"  Files after rename: {len(files_after)}")

    for p in files_after:
        rel = p.relative_to(new_path)
        key = (old, str(rel))

        if key not in before_hashes:
            raise SystemExit(
                f"FAIL: Unexpected asset appeared: {p}"
            )

        after_hash = sha256(p)

        if after_hash != before_hashes[key]:
            raise SystemExit(
                f"FAIL: Asset hash changed: {p}"
            )

        print(f"  HASH PRESERVED: {rel}")

# ---------------------------------------------------------------------
# Validate old/new strings
# ---------------------------------------------------------------------
print("\n[9] OLD/NEW TOKEN VALIDATION")

generator_after = GENERATOR.read_text(encoding="utf-8")
manifest_after = MANIFEST.read_text(encoding="utf-8")

for old, new in CORRECTIONS.items():

    print(f"\n{old}")
    print(f"  Generator old : {generator_after.count(old)}")
    print(f"  Manifest old  : {manifest_after.count(old)}")

    print(f"{new}")
    print(f"  Generator new : {generator_after.count(new)}")
    print(f"  Manifest new  : {manifest_after.count(new)}")

    if generator_after.count(old) != 0:
        raise SystemExit("FAIL: Old generator token remains.")

    if manifest_after.count(old) != 0:
        raise SystemExit("FAIL: Old manifest token remains.")

    if generator_after.count(new) != 1:
        raise SystemExit("FAIL: New generator token count incorrect.")

    if manifest_after.count(new) != 1:
        raise SystemExit("FAIL: New manifest token count incorrect.")

# ---------------------------------------------------------------------
# Final ID preservation
# ---------------------------------------------------------------------
print("\n[10] MICRO ID PRESERVATION")

expected_ids = {
    "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita":
        "ST14_02_M02",

    "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta":
        "ST14_02_M03",
}

for folder_suffix, expected_id in expected_ids.items():
    actual_id = validated[folder_suffix]["micro_id"]

    print(f"{folder_suffix}")
    print(f"  Expected ID : {expected_id}")
    print(f"  Actual ID   : {actual_id}")

    if actual_id != expected_id:
        raise SystemExit(
            f"FAIL: Micro ID changed for {folder_suffix}"
        )

# ---------------------------------------------------------------------
# Final
# ---------------------------------------------------------------------
print("\n" + "=" * 80)
print("SANSKRIT-14 RESULT")
print("=" * 80)

print("PASS — T14 taxonomy mutation completed successfully.")
print()
print("Mutated MicroTopics : 2")
print("Renamed directories  : 2")
print("Updated generator refs : 2")
print("Updated manifest refs  : 2")
print("Micro IDs changed      : 0")
print("Asset files regenerated: 0")
print("Asset hashes changed   : 0")
print()
print("Backups preserved:")
print(f"  {GEN_BACKUP}")
print(f"  {MANIFEST_BACKUP}")
print()
print("No educational content was generated.")

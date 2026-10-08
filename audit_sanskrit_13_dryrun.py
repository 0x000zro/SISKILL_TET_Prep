from pathlib import Path
import json

ROOT = Path("UPTET_CTET/Paper_1_and_2/Sanskrit")
MANIFEST = ROOT / "manifest.json"
GENERATOR = Path("build_sanskrit_framework.py")

CORRECTIONS = {
    "Brihattrayi_Bharavi_Magha_Sriharsha":
        "Brihattrayi_Kiratarjuniya_Sisupalavadha_Naishadhiyacharita",

    "Laghuttrayi_Raghuvamsham_Kumarasambhavam_Megha":
        "Laghutrayi_Raghuvamsham_Kumarasambhavam_Meghaduta",
}

with MANIFEST.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

print("=" * 80)
print("SANSKRIT-13 — T14 TAXONOMY MUTATION DRY-RUN")
print("READ-ONLY — NO FILES WILL BE MODIFIED")
print("=" * 80)

# ------------------------------------------------------------
# Locate exact manifest nodes
# ------------------------------------------------------------
found = {}

for topic in manifest["topics"]:
    if topic["id"] != "T14":
        continue

    for subtopic in topic.get("subtopics", []):
        if subtopic["id"] != "ST14_02":
            continue

        for micro in subtopic.get("micro_topics", []):
            folder = micro["folder"]

            for old, new in CORRECTIONS.items():
                if folder == f"MicroTopic_02_{old}" or \
                   folder == f"MicroTopic_03_{old}":

                    found[old] = {
                        "micro_id": micro["micro_id"],
                        "old_folder": folder,
                        "new_folder": (
                            folder.replace(old, new)
                        ),
                    }

print("\n[1] MANIFEST TARGETS")

for old, new in CORRECTIONS.items():
    print(f"\nOLD : {old}")
    print(f"NEW : {new}")

    if old not in found:
        print("STATUS: NOT FOUND")
        continue

    x = found[old]

    print(f"MICRO ID    : {x['micro_id']}")
    print(f"OLD FOLDER  : {x['old_folder']}")
    print(f"NEW FOLDER  : {x['new_folder']}")
    print("STATUS      : FOUND")

# ------------------------------------------------------------
# Physical directory verification
# ------------------------------------------------------------
print("\n" + "=" * 80)
print("[2] PHYSICAL DIRECTORY TARGETS")
print("=" * 80)

physical_errors = 0

for old, new in CORRECTIONS.items():

    matches = list(ROOT.glob(f"Topic_14_Sanskrit_Literature_Epics_Poets_UPTET/**/MicroTopic_*_{old}"))

    print(f"\nOLD suffix : {old}")
    print(f"Matches    : {len(matches)}")

    for p in matches:
        new_path = p.parent / p.name.replace(old, new)

        print(f"  OLD -> {p}")
        print(f"  NEW -> {new_path}")

        if new_path.exists():
            print("  ERROR: TARGET ALREADY EXISTS")
            physical_errors += 1

# ------------------------------------------------------------
# Generator verification
# ------------------------------------------------------------
print("\n" + "=" * 80)
print("[3] GENERATOR REFERENCES")
print("=" * 80)

generator_text = GENERATOR.read_text(encoding="utf-8")

for old, new in CORRECTIONS.items():
    old_count = generator_text.count(old)
    new_count = generator_text.count(new)

    print(f"\n{old}")
    print(f"  OLD occurrences : {old_count}")
    print(f"  NEW occurrences : {new_count}")

# ------------------------------------------------------------
# Manifest text verification
# ------------------------------------------------------------
print("\n" + "=" * 80)
print("[4] MANIFEST REFERENCES")
print("=" * 80)

manifest_text = MANIFEST.read_text(encoding="utf-8")

for old, new in CORRECTIONS.items():
    print(f"\n{old}")
    print(f"  OLD occurrences : {manifest_text.count(old)}")
    print(f"  NEW occurrences : {manifest_text.count(new)}")

# ------------------------------------------------------------
# Asset inventory
# ------------------------------------------------------------
print("\n" + "=" * 80)
print("[5] ASSET PRESERVATION BASELINE")
print("=" * 80)

asset_counts = {}

for asset in ["Concept", "Short_Notes", "PYQ", "MCQ", "Practice"]:
    asset_counts[asset] = len(
        list(ROOT.glob(
            f"Topic_14_Sanskrit_Literature_Epics_Poets_UPTET/**/"
            f"MicroTopic_*/{asset}/*"
        ))
    )

for asset, count in asset_counts.items():
    print(f"{asset:12}: {count}")

# ------------------------------------------------------------
# Final dry-run gate
# ------------------------------------------------------------
print("\n" + "=" * 80)
print("SANSKRIT-13 DRY-RUN RESULT")
print("=" * 80)

if (
    len(found) == 2
    and physical_errors == 0
    and all(v == 7 for v in asset_counts.values())
):
    print("PASS — mutation plan is safe to execute.")
    print()
    print("NO FILES WERE MODIFIED.")
else:
    print("FAIL — DO NOT MUTATE.")
    print(f"Manifest targets found : {len(found)}/2")
    print(f"Physical target errors : {physical_errors}")

print("\nNEXT GATE:")
print("Do not execute actual mutation until this dry-run returns PASS.")

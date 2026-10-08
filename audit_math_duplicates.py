import os
import hashlib
import json

BASE = "UPTET_CTET/Paper_1_and_2/Mathematics"

ASSETS = [
    ("Concept", "content.md"),
    ("Short_Notes", "content.md"),
    ("PYQ", "content.json"),
    ("MCQ", "content.json"),
    ("Practice", "content.md"),
]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def classify(path):
    if not path or not os.path.isfile(path):
        return "MISSING"

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
    except Exception:
        return "UNREADABLE"

    if not text:
        return "EMPTY"

    if "विषयवस्तु संकलन प्रगति पर है" in text:
        return "PLACEHOLDER"

    if path.endswith(".json"):
        try:
            data = json.loads(text)

            if isinstance(data, dict):
                if data.get("questions") == [] and data.get("total_questions") == 0:
                    return "EMPTY_SCAFFOLD"

                if data.get("items") == []:
                    return "EMPTY_SCAFFOLD"

        except Exception:
            return "INVALID_JSON"

    return "CONTENT"

summary = {
    "topic_dirs": 0,
    "legacy_files": 0,
    "normalized_files": 0,
    "same_hash": 0,
    "different_hash": 0,
    "legacy_placeholder": 0,
    "normalized_placeholder": 0,
    "legacy_empty_scaffold": 0,
    "normalized_empty_scaffold": 0,
    "legacy_content": 0,
    "normalized_content": 0,
    "legacy_missing": 0,
    "normalized_missing": 0,
}

differences = []

topic_dirs = sorted(
    d for d in os.listdir(BASE)
    if d.startswith("Topic_")
    and os.path.isdir(os.path.join(BASE, d))
)

for topic in topic_dirs:
    topic_path = os.path.join(BASE, topic)

    subtopic_dirs = sorted(
        d for d in os.listdir(topic_path)
        if d.startswith("Subtopic_")
        and os.path.isdir(os.path.join(topic_path, d))
    )

    for subtopic in subtopic_dirs:
        subtopic_path = os.path.join(topic_path, subtopic)

        legacy_micros = sorted(
            d for d in os.listdir(subtopic_path)
            if d.startswith("Micro_")
            and os.path.isdir(os.path.join(subtopic_path, d))
        )

        normalized_micros = sorted(
            d for d in os.listdir(subtopic_path)
            if d.startswith("MicroTopic_")
            and os.path.isdir(os.path.join(subtopic_path, d))
        )

        count = max(len(legacy_micros), len(normalized_micros))

        for i in range(count):
            legacy_micro = legacy_micros[i] if i < len(legacy_micros) else None
            normalized_micro = (
                normalized_micros[i]
                if i < len(normalized_micros)
                else None
            )

            for asset, filename in ASSETS:

                legacy_file = (
                    os.path.join(
                        subtopic_path,
                        legacy_micro,
                        asset,
                        filename
                    )
                    if legacy_micro
                    else None
                )

                normalized_file = (
                    os.path.join(
                        subtopic_path,
                        normalized_micro,
                        asset,
                        filename
                    )
                    if normalized_micro
                    else None
                )

                lc = classify(legacy_file)
                nc = classify(normalized_file)

                if lc == "MISSING":
                    summary["legacy_missing"] += 1
                else:
                    summary["legacy_files"] += 1

                if nc == "MISSING":
                    summary["normalized_missing"] += 1
                else:
                    summary["normalized_files"] += 1

                if lc == "PLACEHOLDER":
                    summary["legacy_placeholder"] += 1

                if nc == "PLACEHOLDER":
                    summary["normalized_placeholder"] += 1

                if lc == "EMPTY_SCAFFOLD":
                    summary["legacy_empty_scaffold"] += 1

                if nc == "EMPTY_SCAFFOLD":
                    summary["normalized_empty_scaffold"] += 1

                if lc == "CONTENT":
                    summary["legacy_content"] += 1

                if nc == "CONTENT":
                    summary["normalized_content"] += 1

                if (
                    legacy_file
                    and normalized_file
                    and os.path.isfile(legacy_file)
                    and os.path.isfile(normalized_file)
                ):
                    lh = sha256_file(legacy_file)
                    nh = sha256_file(normalized_file)

                    if lh == nh:
                        summary["same_hash"] += 1
                    else:
                        summary["different_hash"] += 1

                        differences.append({
                            "topic": topic,
                            "subtopic": subtopic,
                            "legacy_micro": legacy_micro,
                            "normalized_micro": normalized_micro,
                            "asset": asset,
                            "legacy_class": lc,
                            "normalized_class": nc,
                            "legacy_size": os.path.getsize(legacy_file),
                            "normalized_size": os.path.getsize(normalized_file),
                        })

    summary["topic_dirs"] += 1

print()
print("=" * 70)
print("SISKILL — MATH LEGACY vs NORMALIZED FORENSIC AUDIT")
print("=" * 70)

print()
print("SUMMARY")
print("-" * 70)

for key, value in summary.items():
    print(f"{key:30}: {value}")

print()
print("DIFFERENT FILES")
print("-" * 70)

if differences:
    for d in differences:
        print(
            f"{d['topic']} | "
            f"{d['subtopic']} | "
            f"{d['asset']} | "
            f"{d['legacy_class']} -> {d['normalized_class']} | "
            f"{d['legacy_size']} -> {d['normalized_size']}"
        )
else:
    print("No file differences found.")

print()
print("=" * 70)
print("AUDIT COMPLETE — NO PROJECT FILES WERE MODIFIED")
print("=" * 70)

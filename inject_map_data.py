"""
Reads map_data.json and injects 'level' and 'topic' into each
corresponding words/<key>/data.json file.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
WORDS_DIR = os.path.join(BASE_DIR, "words")


def main():
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    updated = 0
    skipped = 0
    missing = 0

    for folder_name, meta in map_data.items():
        data_path = os.path.join(WORDS_DIR, folder_name, "data.json")

        if not os.path.isfile(data_path):
            print(f"[MISSING] {data_path}")
            missing += 1
            continue

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if already has both fields with same values
        if data.get("level") == meta["level"] and data.get("topic") == meta["topic"]:
            skipped += 1
            continue

        data["level"] = meta["level"]
        data["topic"] = meta["topic"]

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        updated += 1

    print(f"\nDone!")
    print(f"  Updated: {updated}")
    print(f"  Skipped (already up-to-date): {skipped}")
    print(f"  Missing data.json: {missing}")
    print(f"  Total entries in map_data: {len(map_data)}")


if __name__ == "__main__":
    main()

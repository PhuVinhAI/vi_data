"""
Reverts the restructured words/ directory back to flat structure:
  words/<topic>/<level>/<word_folder>/  →  words/<word_folder>/

Then removes the now-empty level/topic directories.
"""

import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
WORDS_DIR = os.path.join(BASE_DIR, "words")


def main():
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    moved = 0
    skipped = 0
    missing = 0

    for folder_name, meta in map_data.items():
        level = meta["level"]
        topic = meta["topic"]

        src = os.path.join(WORDS_DIR, topic, level, folder_name)
        dest = os.path.join(WORDS_DIR, folder_name)

        if not os.path.isdir(src):
            # Maybe already flat
            if os.path.isdir(dest):
                skipped += 1
            else:
                print(f"[MISSING] {src}")
                missing += 1
            continue

        if os.path.exists(dest):
            print(f"[EXISTS] {dest} — skipping")
            skipped += 1
            continue

        shutil.move(src, dest)
        moved += 1

    # Clean up empty topic and level directories
    removed_dirs = 0
    for level_dir in os.listdir(WORDS_DIR):
        level_path = os.path.join(WORDS_DIR, level_dir)
        if not os.path.isdir(level_path):
            continue
        # Skip word folders (they start with digits like 0001_)
        if level_dir[0].isdigit():
            continue
        for topic_dir in os.listdir(level_path):
            topic_path = os.path.join(level_path, topic_dir)
            if os.path.isdir(topic_path) and not os.listdir(topic_path):
                os.rmdir(topic_path)
                removed_dirs += 1
        if os.path.isdir(level_path) and not os.listdir(level_path):
            os.rmdir(level_path)
            removed_dirs += 1

    print(f"\nDone!")
    print(f"  Moved back: {moved}")
    print(f"  Skipped: {skipped}")
    print(f"  Missing: {missing}")
    print(f"  Empty dirs removed: {removed_dirs}")


if __name__ == "__main__":
    main()

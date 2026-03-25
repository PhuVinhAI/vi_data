"""
Restructures the flat words/ directory into a hierarchy:
  words/<topic>/<level>/<word_folder>/

Example:
  words/0001_là/data.json  →  words/Core Verbs/A1/0001_là/data.json

Uses map_data.json as the source of truth for level & topic.
Run with --dry-run to preview changes without moving anything.
"""

import json
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
WORDS_DIR = os.path.join(BASE_DIR, "words")


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE (no files will be moved) ===\n")

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    moved = 0
    skipped = 0
    missing = 0

    for folder_name, meta in map_data.items():
        level = meta["level"]
        topic = meta["topic"]

        src = os.path.join(WORDS_DIR, folder_name)

        if not os.path.isdir(src):
            print(f"[MISSING] {src}")
            missing += 1
            continue

        dest_dir = os.path.join(WORDS_DIR, topic, level)
        dest = os.path.join(dest_dir, folder_name)

        # Already in correct location
        if os.path.normpath(src) == os.path.normpath(dest):
            skipped += 1
            continue

        # Destination already exists (e.g. from a previous partial run)
        if os.path.exists(dest):
            print(f"[EXISTS] {dest} — skipping")
            skipped += 1
            continue

        if dry_run:
            print(f"  {folder_name}  →  {topic}/{level}/{folder_name}")
        else:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src, dest)

        moved += 1

    print(f"\nDone!")
    print(f"  {'Would move' if dry_run else 'Moved'}: {moved}")
    print(f"  Skipped: {skipped}")
    print(f"  Missing source: {missing}")
    print(f"  Total entries in map_data: {len(map_data)}")

    if dry_run and moved > 0:
        print(f"\nRun without --dry-run to execute the moves.")


if __name__ == "__main__":
    main()

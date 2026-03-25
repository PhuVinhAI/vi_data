"""
Merges similar/small topics in map_data.json into broader categories.
Creates a backup before modifying. Run with --dry-run to preview.

Merge rules:
  58 topics → ~35 merged topics
  Goal: every level/topic combo has >= 3 words
"""

import json
import os
import shutil
import sys
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
BACKUP_FILE = os.path.join(BASE_DIR, "map_data.backup.json")

# ── Merge mapping: old topic → new topic ──
MERGE_MAP = {
    # Daily Life consolidation (99 → 1 group)
    "Daily Life & Objects":   "Daily Life",
    "Daily Life & Services":  "Daily Life",
    "Daily Life & Chores":    "Daily Life",

    # Nature consolidation (61 → 1 group)
    "Nature & Weather":       "Nature",
    "Nature & Animals":       "Nature",
    "Nature & Plants":        "Nature",

    # Culture & Religion consolidation (31 → 1 group)
    "Culture & Beliefs":      "Culture & Traditions",
    "History & Culture":      "Culture & Traditions",
    "Religion & Beliefs":     "Culture & Traditions",

    # Conversational consolidation (81 → 1 group)
    "Conversational Particles": "Conversation",
    "Conversational Phrases":   "Conversation",
    "Conversational Sounds":    "Conversation",
    "Greetings & Politeness":   "Conversation",

    # Places consolidation (132 → 1 group)
    "Places & Directions":    "Places",
    "Places & Locations":     "Places",

    # Pronouns consolidation (45 → 1 group)
    "Pronouns & Titles":        "Pronouns",
    "Pronouns & Demonstratives": "Pronouns",

    # Emotions consolidation (153 → 1 group)
    "Emotions & Relationships": "Emotions & Feelings",

    # Society consolidation (91 → 1 group)
    "Society & Events":       "Society & Culture",

    # Time consolidation (108 → 1 group)
    "Time & Tenses":          "Time",
    "Time & Dates":           "Time",

    # Entertainment consolidation (80+17 → 1 group)
    "Hobbies & Entertainment": "Entertainment",
    "Media & Entertainment":   "Entertainment",
    "Sports & Games":          "Entertainment",

    # Health consolidation (100 → 1 group)
    "Medical & Health":       "Body & Health",

    # Adjectives mega-group (208 → 1 group)
    "Colors & Shapes":        "Adjectives & Descriptions",
    "Comparisons":            "Adjectives & Descriptions",

    # Adverbs consolidation (67 → 1 group)
    "Adverbs of Degree":      "Adverbs",
    "Adverbs of Frequency":   "Adverbs",

    # Work consolidation (192 → 1 group)
    "Work & Jobs":            "Work & Education",

    # Grammar mega-group (29+8+20 → 1 group)
    "Prepositions":           "Grammar & Particles",
    "Negation & Questions":   "Grammar & Particles",
    "Conjunctions & Connectors": "Grammar & Particles",

    # Shopping into Daily Life (29 → merge)
    "Shopping & Services":    "Daily Life",

    # Family into People (35+36 → 1 group)
    "Family & Relatives":     "People & Relationships",

    # Quantifiers into Numbers (50 → merge)
    "Quantifiers & Classifiers": "Numbers & Quantifiers",

    # Small combos: absorb into closest large group
    "Abstract Concepts":      "Thoughts & Opinions",
    "Crime & Law":            "Society & Culture",
}


def main():
    dry_run = "--dry-run" in sys.argv

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    # Count changes
    changed = 0
    unchanged = 0
    changes_detail = defaultdict(int)

    for key, meta in map_data.items():
        old_topic = meta["topic"]
        new_topic = MERGE_MAP.get(old_topic, old_topic)

        if new_topic != old_topic:
            changes_detail[f"{old_topic} → {new_topic}"] += 1
            if not dry_run:
                meta["topic"] = new_topic
            changed += 1
        else:
            unchanged += 1

    # Show summary
    if dry_run:
        print("=== DRY RUN MODE ===\n")

    # Count new topics
    if dry_run:
        new_topics = Counter()
        for key, meta in map_data.items():
            t = MERGE_MAP.get(meta["topic"], meta["topic"])
            new_topics[t] += 1
    else:
        new_topics = Counter(meta["topic"] for meta in map_data.values())

    old_topics = set()
    for meta in map_data.values():
        old_topics.add(meta.get("_old_topic", meta["topic"]))

    print("Merge details:")
    for change, count in sorted(changes_detail.items()):
        print(f"  {change}: {count} words")

    print(f"\n  Total changed: {changed}")
    print(f"  Total unchanged: {unchanged}")
    print(f"  Topics: 58 → {len(new_topics)}")

    # Show new topic distribution per level
    if dry_run:
        level_topic = defaultdict(lambda: defaultdict(int))
        for key, meta in map_data.items():
            t = MERGE_MAP.get(meta["topic"], meta["topic"])
            level_topic[meta["level"]][t] += 1
    else:
        level_topic = defaultdict(lambda: defaultdict(int))
        for key, meta in map_data.items():
            level_topic[meta["level"]][meta["topic"]] += 1

    print("\nNew distribution (topics with <= 3 words per level):")
    still_small = 0
    for level in ["A1", "A2", "B1", "B2"]:
        small = {t: c for t, c in level_topic[level].items() if c <= 3}
        if small:
            for t, c in sorted(small.items()):
                print(f"  [{level}] {t}: {c} word(s)")
                still_small += 1
    if still_small == 0:
        print("  ✓ None! All topic/level combos have >= 4 words.")
    else:
        print(f"  Still {still_small} small combos remaining.")

    if not dry_run:
        # Backup
        shutil.copy2(MAP_FILE, BACKUP_FILE)
        print(f"\nBackup saved to: {BACKUP_FILE}")

        with open(MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(map_data, f, ensure_ascii=False, indent=2)

        print("map_data.json updated!")
    else:
        print(f"\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()

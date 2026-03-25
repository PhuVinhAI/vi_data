"""
Reclassifies all words in map_data.json into ~25 well-balanced topics
designed for a Vietnamese learning app for foreigners.

Creates backup before modifying. Run with --dry-run to preview.

Target: 58 topics → 25 topics, balanced per level, no 1-word combos.
"""

import json
import os
import shutil
import sys
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
BACKUP_FILE = os.path.join(BASE_DIR, "map_data.backup.json")

# ── Reclassification: old topic → new topic ──
# Topics NOT listed here keep their original name.
RECLASSIFY = {
    # ─── Descriptions (208 words) ───
    "Adjectives & Descriptions": "Descriptions",
    "Colors & Shapes":           "Descriptions",
    "Comparisons":               "Descriptions",

    # ─── Adverbs (67 words) ───
    "Adverbs of Degree":    "Adverbs",
    "Adverbs of Frequency": "Adverbs",

    # ─── Grammar (110 words) ───
    "Grammar & Particles":       "Grammar",
    "Conjunctions & Connectors": "Grammar",
    "Negation & Questions":      "Grammar",
    "Prepositions":              "Grammar",

    # ─── Numbers & Counting (115 words) ───
    "Numbers & Quantifiers":     "Numbers & Counting",
    "Quantifiers & Classifiers": "Numbers & Counting",

    # ─── Pronouns (45 words) ───
    "Pronouns & Titles":         "Pronouns",
    "Pronouns & Demonstratives": "Pronouns",

    # ─── Time (108 words) ───
    "Time & Dates":  "Time",
    "Time & Tenses": "Time",

    # ─── People & Family (71 words) ───
    "People & Relationships": "People & Family",
    "Family & Relatives":     "People & Family",

    # ─── Emotions (153 words) ───
    "Emotions & Relationships": "Emotions & Feelings",

    # ─── Thoughts & Ideas (280 words) ───
    "Abstract Concepts":  "Thoughts & Ideas",
    "Thoughts & Opinions": "Thoughts & Ideas",

    # ─── Daily Life (128 words) ───
    "Daily Life & Objects":  "Daily Life",
    "Daily Life & Services": "Daily Life",
    "Daily Life & Chores":   "Daily Life",
    "Shopping & Services":   "Daily Life",

    # ─── Body & Health (100 words) ───
    "Medical & Health": "Body & Health",

    # ─── Places & Travel (164 words) ───
    "Places & Directions": "Places & Travel",
    "Places & Locations":  "Places & Travel",
    "Travel & Transport":  "Places & Travel",

    # ─── Nature (61 words) ───
    "Nature & Weather": "Nature",
    "Nature & Animals": "Nature",
    "Nature & Plants":  "Nature",

    # ─── Conversation (98 words) ───
    "Conversational Particles": "Conversation",
    "Conversational Phrases":   "Conversation",
    "Conversational Sounds":    "Conversation",
    "Greetings & Politeness":   "Conversation",

    # ─── Entertainment (125 words) ───
    "Hobbies & Entertainment": "Entertainment",
    "Media & Entertainment":   "Entertainment",
    "Sports & Games":          "Entertainment",
    "Fantasy & Fiction":       "Entertainment",

    # ─── Work & Career (192 words) ───
    "Work & Education": "Work & Career",
    "Work & Jobs":      "Work & Career",

    # ─── Culture & Society (155 words) ───
    "Society & Culture":    "Culture & Society",
    "Society & Events":     "Culture & Society",
    "Culture & Traditions": "Culture & Society",
    "Culture & Beliefs":    "Culture & Society",
    "History & Culture":    "Culture & Society",
    "Religion & Beliefs":   "Culture & Society",
    "Crime & Law":          "Culture & Society",

    # ─── Keep as-is ───
    # "Actions & Behaviors"    347  (keep)
    # "Emotions & Feelings"    153  (keep, absorbs Emotions & Relationships)
    # "Business & Economy"     125  (keep)
    # "Science & Tech"          78  (keep)
    # "Social Interactions"     78  (keep)
    # "Personality & Traits"    58  (keep)
    # "Slang & Colloquialisms"  41  (keep - useful for learners)
    # "Core Verbs"              32  (keep - essential for beginners)
    # "Food & Drinks"           67  (keep)
    # "Body & Health"          100  (keep, absorbs Medical)
}


def main():
    dry_run = "--dry-run" in sys.argv

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    if dry_run:
        print("=== DRY RUN MODE ===\n")

    changed = 0
    changes_detail = defaultdict(int)

    for key, meta in map_data.items():
        old_topic = meta["topic"]
        new_topic = RECLASSIFY.get(old_topic, old_topic)

        if new_topic != old_topic:
            changes_detail[f"{old_topic} → {new_topic}"] += 1
            if not dry_run:
                meta["topic"] = new_topic
            changed += 1

    # Calculate new distribution
    def get_topic(meta):
        return RECLASSIFY.get(meta["topic"], meta["topic"]) if dry_run else meta["topic"]

    new_topics = Counter(get_topic(m) for m in map_data.values())
    level_topic = defaultdict(lambda: defaultdict(int))
    for meta in map_data.values():
        level_topic[meta["level"]][get_topic(meta)] += 1

    # Print merge details
    print("Reclassification details:")
    for change, count in sorted(changes_detail.items()):
        print(f"  {change}: {count} words")
    print(f"\n  Total reclassified: {changed}")
    print(f"  Topics: 58 → {len(new_topics)}")

    # Print new topic sizes
    print(f"\n{'─'*60}")
    print(f"{'Topic':<30} {'Total':>6}  {'A1':>4} {'A2':>4} {'B1':>4} {'B2':>4}")
    print(f"{'─'*60}")
    for topic, total in sorted(new_topics.items(), key=lambda x: -x[1]):
        a1 = level_topic["A1"].get(topic, 0)
        a2 = level_topic["A2"].get(topic, 0)
        b1 = level_topic["B1"].get(topic, 0)
        b2 = level_topic["B2"].get(topic, 0)
        flags = []
        for l, c in [("A1", a1), ("A2", a2), ("B1", b1), ("B2", b2)]:
            if 0 < c <= 2:
                flags.append(f"⚠️ {l}={c}")
        flag_str = f"  {'  '.join(flags)}" if flags else ""
        print(f"  {topic:<28} {total:>6}  {a1:>4} {a2:>4} {b1:>4} {b2:>4}{flag_str}")
    print(f"{'─'*60}")
    print(f"  {'TOTAL':<28} {sum(new_topics.values()):>6}  "
          f"{sum(level_topic['A1'].values()):>4} "
          f"{sum(level_topic['A2'].values()):>4} "
          f"{sum(level_topic['B1'].values()):>4} "
          f"{sum(level_topic['B2'].values()):>4}")

    # Count problems
    problems = 0
    for level in ["A1", "A2", "B1", "B2"]:
        for topic, count in level_topic[level].items():
            if 0 < count <= 2:
                problems += 1

    print(f"\n  Combos with ≤2 words: {problems}")
    if problems == 0:
        print("  ✅ Perfect distribution!")

    if not dry_run:
        shutil.copy2(MAP_FILE, BACKUP_FILE)
        print(f"\n  Backup: {BACKUP_FILE}")
        with open(MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(map_data, f, ensure_ascii=False, indent=2)
        print("  ✅ map_data.json updated!")
    else:
        print(f"\n  Run without --dry-run to apply.")


if __name__ == "__main__":
    main()

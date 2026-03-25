"""
Reclassifies all 3006 words into 20 CEFR-aligned thematic topics,
based on Thông tư 17/2015/TT-BGDĐT (Khung năng lực tiếng Việt).

CEFR organizes vocabulary by COMMUNICATIVE CONTEXT, not by word class.
Topics match A1-A2 themes (gia đình, mua hàng, hỏi đường, việc làm)
and B1-B2 themes (công việc, giải trí, chuyên môn).

Creates backup before modifying. Run with --dry-run to preview.
"""

import json
import os
import shutil
import sys
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
BACKUP_FILE = os.path.join(BASE_DIR, "map_data.backup.json")

# ══════════════════════════════════════════════════════════════
# 20 CEFR-aligned topics  (old 58 → new 20)
#
# Thông tư A1-A2 contexts:
#   bản thân, gia đình, mua hàng, hỏi đường, việc làm,
#   môi trường xung quanh, nhu cầu thiết yếu
# Thông tư B1-B2 contexts:
#   công việc, trường học, giải trí, chuyên môn, xã hội
# ══════════════════════════════════════════════════════════════

RECLASSIFY = {
    # ─── 1. Greetings & Communication (176 words) ───
    # A1-A2 core: chào hỏi, giới thiệu, giao tiếp cơ bản
    "Greetings & Politeness":     "Greetings & Communication",
    "Conversational Particles":   "Greetings & Communication",
    "Conversational Phrases":     "Greetings & Communication",
    "Conversational Sounds":      "Greetings & Communication",
    "Social Interactions":        "Greetings & Communication",

    # ─── 2. Family & People (116 words) ───
    # A1: bản thân, người thân, bạn bè
    "Family & Relatives":         "Family & People",
    "People & Relationships":     "Family & People",
    "Pronouns & Titles":          "Family & People",
    "Pronouns & Demonstratives":  "Family & People",

    # ─── 3. Home & Daily Life (128 words) ───
    # A1-A2: nhà cửa, sinh hoạt, mua sắm, dịch vụ
    "Daily Life & Objects":       "Home & Daily Life",
    "Daily Life & Services":      "Home & Daily Life",
    "Daily Life & Chores":        "Home & Daily Life",
    "Shopping & Services":        "Home & Daily Life",

    # ─── 4. Food & Drinks (67 words) ───
    # A1-A2: ăn uống, nấu ăn
    "Food & Drinks":              "Food & Drinks",

    # ─── 5. Places & Transportation (164 words) ───
    # A2: hỏi đường, địa điểm; B1: du lịch
    "Places & Directions":        "Places & Transportation",
    "Places & Locations":         "Places & Transportation",
    "Travel & Transport":         "Places & Transportation",

    # ─── 6. Time & Schedules (108 words) ───
    # A1-A2: thời gian, ngày tháng, lịch trình
    "Time & Dates":               "Time & Schedules",
    "Time & Tenses":              "Time & Schedules",

    # ─── 7. Health & Body (100 words) ───
    # A2-B1: sức khỏe, cơ thể, y tế
    "Body & Health":              "Health & Body",
    "Medical & Health":           "Health & Body",

    # ─── 8. Nature & Environment (61 words) ───
    # A2: môi trường xung quanh, thời tiết
    "Nature & Weather":           "Nature & Environment",
    "Nature & Animals":           "Nature & Environment",
    "Nature & Plants":            "Nature & Environment",

    # ─── 9. Work & Education (192 words) ───
    # A2: việc làm; B1: trường học, công việc
    "Work & Education":           "Work & Education",
    "Work & Jobs":                "Work & Education",

    # ─── 10. Entertainment & Hobbies (125 words) ───
    # B1: giải trí
    "Hobbies & Entertainment":    "Entertainment & Hobbies",
    "Media & Entertainment":      "Entertainment & Hobbies",
    "Sports & Games":             "Entertainment & Hobbies",
    "Fantasy & Fiction":          "Entertainment & Hobbies",

    # ─── 11. Culture & Society (155 words) ───
    # B1-B2: văn hóa, xã hội, pháp luật
    "Society & Culture":          "Culture & Society",
    "Society & Events":           "Culture & Society",
    "Culture & Traditions":       "Culture & Society",
    "Culture & Beliefs":          "Culture & Society",
    "History & Culture":          "Culture & Society",
    "Religion & Beliefs":         "Culture & Society",
    "Crime & Law":                "Culture & Society",

    # ─── 12. Emotions & Personality (211 words) ───
    # A2-B2: cảm xúc, tính cách, quan hệ tình cảm
    "Emotions & Feelings":        "Emotions & Personality",
    "Emotions & Relationships":   "Emotions & Personality",
    "Personality & Traits":       "Emotions & Personality",

    # ─── 13. Business & Economy (125 words) ───
    # B2: chuyên môn kinh doanh
    "Business & Economy":         "Business & Economy",

    # ─── 14. Science & Technology (78 words) ───
    # B1-B2: chuyên môn khoa học
    "Science & Tech":             "Science & Technology",

    # ─── 15. Descriptions (208 words) ───
    # A1-B2: mô tả, tính chất, so sánh
    "Adjectives & Descriptions":  "Descriptions",
    "Colors & Shapes":            "Descriptions",
    "Comparisons":                "Descriptions",

    # ─── 16. Thinking & Ideas (280 words) ───
    # B1-B2: tư duy, quan điểm, khái niệm
    "Thoughts & Opinions":        "Thinking & Ideas",
    "Abstract Concepts":          "Thinking & Ideas",

    # ─── 17. Actions & Activities (379 words) ───
    # A1-B2: các hành động, hoạt động
    "Actions & Behaviors":        "Actions & Activities",
    "Core Verbs":                 "Actions & Activities",

    # ─── 18. Numbers & Measurement (115 words) ───
    # A1-A2: số đếm, đo lường, lượng từ
    "Numbers & Quantifiers":      "Numbers & Measurement",
    "Quantifiers & Classifiers":  "Numbers & Measurement",

    # ─── 19. Grammar & Connectors (177 words) ───
    # A1-B2: từ chức năng, liên kết, trạng từ
    "Grammar & Particles":        "Grammar & Connectors",
    "Conjunctions & Connectors":  "Grammar & Connectors",
    "Negation & Questions":       "Grammar & Connectors",
    "Prepositions":               "Grammar & Connectors",
    "Adverbs of Degree":          "Grammar & Connectors",
    "Adverbs of Frequency":       "Grammar & Connectors",

    # ─── 20. Slang & Colloquialisms (41 words) ───
    # B1-B2: tiếng lóng, khẩu ngữ
    "Slang & Colloquialisms":     "Slang & Colloquialisms",
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

    # Print merge summary
    print(f"Reclassified: {changed} words")
    print(f"Topics: 58 → {len(new_topics)}")

    # Print distribution table
    print(f"\n{'─'*70}")
    print(f"  {'#':>2}  {'Topic':<30} {'Total':>5}  {'A1':>4} {'A2':>4} {'B1':>4} {'B2':>4}")
    print(f"{'─'*70}")

    for i, (topic, total) in enumerate(
        sorted(new_topics.items(), key=lambda x: -x[1]), 1
    ):
        a1 = level_topic["A1"].get(topic, 0)
        a2 = level_topic["A2"].get(topic, 0)
        b1 = level_topic["B1"].get(topic, 0)
        b2 = level_topic["B2"].get(topic, 0)
        flags = []
        for l, c in [("A1", a1), ("A2", a2), ("B1", b1), ("B2", b2)]:
            if 0 < c <= 2:
                flags.append(f"⚠️{l}={c}")
        flag_str = f"  {'  '.join(flags)}" if flags else ""
        print(f"  {i:>2}  {topic:<30} {total:>5}  {a1:>4} {a2:>4} {b1:>4} {b2:>4}{flag_str}")

    print(f"{'─'*70}")
    print(f"      {'TOTAL':<30} {sum(new_topics.values()):>5}  "
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

    # CEFR alignment check
    print(f"\n{'─'*70}")
    print("  CEFR Alignment Check (Thông tư 17/2015):")
    a1_topics = [t for t, c in level_topic["A1"].items() if c >= 3]
    a2_topics = [t for t, c in level_topic["A2"].items() if c >= 3]
    print(f"  A1 topics (≥3 words): {len(a1_topics)}")
    print(f"  A2 topics (≥3 words): {len(a2_topics)}")
    print(f"  B1 topics (≥3 words): {len([t for t, c in level_topic['B1'].items() if c >= 3])}")
    print(f"  B2 topics (≥3 words): {len([t for t, c in level_topic['B2'].items() if c >= 3])}")

    # A1 should cover: bản thân, gia đình, nhu cầu cơ bản
    required_a1 = ["Family & People", "Food & Drinks", "Home & Daily Life",
                   "Actions & Activities", "Time & Schedules"]
    print(f"\n  A1 required topics present:")
    for t in required_a1:
        count = level_topic["A1"].get(t, 0)
        status = "✅" if count >= 3 else "❌"
        print(f"    {status} {t}: {count} words")

    # A2 should cover: gia đình, mua hàng, hỏi đường, việc làm
    required_a2 = ["Family & People", "Home & Daily Life",
                   "Places & Transportation", "Work & Education"]
    print(f"\n  A2 (Bậc 2) — gia đình, mua hàng, hỏi đường, việc làm:")
    for t in required_a2:
        count = level_topic["A2"].get(t, 0)
        status = "✅" if count >= 5 else "❌"
        print(f"    {status} {t}: {count} words")

    # B1 should cover: công việc, trường học, giải trí, kinh nghiệm
    required_b1 = ["Work & Education", "Entertainment & Hobbies",
                   "Greetings & Communication", "Thinking & Ideas",
                   "Emotions & Personality", "Culture & Society"]
    print(f"\n  B1 (Bậc 3) — công việc, trường học, giải trí, kinh nghiệm:")
    for t in required_b1:
        count = level_topic["B1"].get(t, 0)
        status = "✅" if count >= 5 else "❌"
        print(f"    {status} {t}: {count} words")

    # B2 should cover: chuyên môn, đa dạng chủ đề, quan điểm
    required_b2 = ["Business & Economy", "Science & Technology",
                   "Thinking & Ideas", "Culture & Society",
                   "Work & Education", "Actions & Activities"]
    print(f"\n  B2 (Bậc 4) — chuyên môn, đa dạng chủ đề, quan điểm:")
    for t in required_b2:
        count = level_topic["B2"].get(t, 0)
        status = "✅" if count >= 5 else "❌"
        print(f"    {status} {t}: {count} words")

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

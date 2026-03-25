"""
Applies corrections based on Thông tư 17/2015 review:
1. Restore map_data.json from backup (original 58 topics)
2. Apply word-level overrides (level + topic changes)
   - Particles → A1/A2
   - Slang → C1
   - Grammar kept as sub-categories
"""

import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = os.path.join(BASE_DIR, "map_data.json")
BACKUP_FILE = os.path.join(BASE_DIR, "map_data.backup.json")

# ── Word-level overrides (from Thông tư 17/2015 review) ──
OVERRIDES = {
    # === Particles → A1/A2 (sinh hoạt cơ bản) ===
    "0080_thôi":      {"level": "A2", "topic": "Conversational Particles"},
    "0128_chứ":       {"level": "A2", "topic": "Conversational Particles"},
    "0165_à":         {"level": "A2", "topic": "Conversational Particles"},
    "0224_á":         {"level": "A2", "topic": "Conversational Particles"},
    "0261_nha":       {"level": "A2", "topic": "Conversational Particles"},
    "0400_nè":        {"level": "A2", "topic": "Conversational Particles"},
    "0401_hở":        {"level": "A2", "topic": "Conversational Particles"},
    "0550_nhỉ":       {"level": "A2", "topic": "Conversational Particles"},
    "0551_á_nha":     {"level": "A2", "topic": "Conversational Particles"},
    "0656_hả":        {"level": "A2", "topic": "Conversational Particles"},
    "0676_nhá":       {"level": "A2", "topic": "Conversational Particles"},
    "1552_ủa":        {"level": "A2", "topic": "Conversational Particles"},
    "1601_ôi":        {"level": "A2", "topic": "Conversational Particles"},
    "1690_ờ":         {"level": "A2", "topic": "Conversational Particles"},
    "2199_ồ":         {"level": "A2", "topic": "Conversational Particles"},
    "2321_ừm":        {"level": "A2", "topic": "Conversational Particles"},
    "2954_ơ":         {"level": "A2", "topic": "Conversational Particles"},

    # === Conversational Phrases → level adjustments ===
    "0121_đi_đi":     {"level": "A2", "topic": "Conversational Phrases"},
    "0338_làm_vậy":   {"level": "A2", "topic": "Conversational Phrases"},
    "0414_như_vậy":    {"level": "A2", "topic": "Conversational Phrases"},
    "0509_thôi_nha":  {"level": "A2", "topic": "Conversational Phrases"},
    "0566_ơi_trời":   {"level": "A2", "topic": "Conversational Phrases"},
    "0568_xíu_nha":   {"level": "A2", "topic": "Conversational Phrases"},
    "0686_nói_gì":    {"level": "A2", "topic": "Conversational Phrases"},
    "0811_ây_da":      {"level": "A2", "topic": "Conversational Phrases"},
    "0974_nói_nhỏ":   {"level": "A2", "topic": "Conversational Phrases"},
    "1022_ừ_ừ":       {"level": "A2", "topic": "Conversational Phrases"},
    "1090_vậy_nha":   {"level": "A2", "topic": "Conversational Phrases"},
    "1147_vậy_hả":    {"level": "A2", "topic": "Conversational Phrases"},
    "1630_trời_ơi":   {"level": "A2", "topic": "Conversational Phrases"},
    "2402_vậy_là":    {"level": "A2", "topic": "Conversational Phrases"},
    "2454_kìa":       {"level": "A2", "topic": "Conversational Phrases"},

    # === Greetings → A1 ===
    "0587_dạ_dạ":     {"level": "A1", "topic": "Greetings & Politeness"},
    "0953_chào_bác":  {"level": "A1", "topic": "Greetings & Politeness"},

    # === Time & Tenses fix ===
    "0142_xong":      {"level": "A1", "topic": "Time & Tenses"},

    # === Negation fix ===
    "0704_chẳng":     {"level": "B1", "topic": "Negation & Questions"},

    # === Slang → C1 (Bậc 5: thành ngữ, tiếng lóng) ===
    "0061_đại_ca":    {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0073_sư_phụ":    {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0212_đệ":        {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0385_giang_hồ":  {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0390_bánh_bèo":  {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0431_biến_thái":  {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0603_đệ_tử":    {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0759_bảo_kê":    {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0786_bá_đạo":    {"level": "C1", "topic": "Slang & Colloquialisms"},
    "0835_đại_gia":   {"level": "C1", "topic": "Slang & Colloquialisms"},
    "1048_huynh_đệ":  {"level": "C1", "topic": "Slang & Colloquialisms"},
    "2507_chế":       {"level": "C1", "topic": "Slang & Colloquialisms"},

    # === Slang kept at B1/B2 (colloquial but common) ===
    "0329_dô":        {"level": "B1", "topic": "Slang & Colloquialisms"},
    "0580_ké":        {"level": "B1", "topic": "Slang & Colloquialisms"},
    "0637_tùm_lum":   {"level": "B1", "topic": "Slang & Colloquialisms"},
    "0908_bậy_bạ":    {"level": "B1", "topic": "Slang & Colloquialisms"},
    "1208_thiệt":     {"level": "B1", "topic": "Slang & Colloquialisms"},
    "2582_bồ":        {"level": "B1", "topic": "Slang & Colloquialisms"},
    "2924_nhậu":      {"level": "B1", "topic": "Slang & Colloquialisms"},
}


def main():
    # Step 1: Restore from backup
    if not os.path.isfile(BACKUP_FILE):
        print(f"ERROR: Backup not found: {BACKUP_FILE}")
        return

    shutil.copy2(BACKUP_FILE, MAP_FILE)
    print(f"✅ Restored from backup (original 58 topics)")

    # Step 2: Apply word-level overrides
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    applied = 0
    missing = 0
    level_changes = 0
    topic_changes = 0

    for key, override in OVERRIDES.items():
        if key not in map_data:
            print(f"  [MISSING] {key}")
            missing += 1
            continue

        old = map_data[key]
        if old["level"] != override["level"]:
            level_changes += 1
        if old["topic"] != override["topic"]:
            topic_changes += 1
        map_data[key] = override
        applied += 1

    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Applied {applied} overrides ({missing} missing)")
    print(f"   Level changes: {level_changes}")
    print(f"   Topic changes: {topic_changes}")

    # Step 3: Show new level distribution
    from collections import Counter, defaultdict
    levels = Counter(m["level"] for m in map_data.values())
    topics = Counter(m["topic"] for m in map_data.values())

    print(f"\n── Level distribution ──")
    for l in sorted(levels):
        print(f"  {l}: {levels[l]} words")

    print(f"\n── Topics: {len(topics)} unique ──")
    print(f"  (run reclassify_topics.py --dry-run to see full table)")


if __name__ == "__main__":
    main()

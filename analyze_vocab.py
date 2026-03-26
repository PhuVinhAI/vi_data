import os
import json
from collections import Counter

# Đường dẫn cấu hình
BASE_DIR = r"c:\Users\tomis\Docs\vi_data"
WORDS_DIR = os.path.join(BASE_DIR, "words")
REPORT_DIR = os.path.join(BASE_DIR, "report")
REPORT_FILE = os.path.join(REPORT_DIR, "report.md")

def analyze_data():
    all_data = []
    
    if not os.path.exists(WORDS_DIR):
        print(f"Lỗi: Không tìm thấy thư mục {WORDS_DIR}")
        return

    for folder in os.listdir(WORDS_DIR):
        json_path = os.path.join(WORDS_DIR, folder, "data.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    all_data.append({
                        'rank': content.get('rank'),
                        'level': content.get('level', 'N/A'),
                        'topic': content.get('topic', 'Uncategorized'),
                        'word': content.get('word', folder)
                    })
            except Exception:
                continue

    all_data.sort(key=lambda x: x['rank'] if x['rank'] is not None else 9999)

    thresholds = [50, 100, 250, 500]
    
    # Ghi file báo cáo Markdown
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Báo cáo Phân tích Dữ liệu Từ vựng Tiếng Việt\n\n")
        f.write(f"Phân tích tổng hợp từ {len([x for x in all_data if x['rank'] is not None])} từ vựng.\n\n")

        for t in thresholds:
            group = [d for d in all_data if d['rank'] is not None and d['rank'] <= t]
            total = len(group)
            
            f.write(f"## NHÓM {t} TỪ ĐẦU TIÊN (RANK 1-{t})\n\n")
            
            # --- PHÂN TÍCH TRÌNH ĐỘ ---
            f.write("### 1. Phân bổ Trình độ (CEFR)\n")
            level_counts = Counter([d['level'] for d in group])
            for lvl in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'N/A']:
                count = level_counts.get(lvl, 0)
                if count > 0 or lvl in ['A1', 'A2', 'B1']:
                    percent = (count / total * 100) if total > 0 else 0
                    f.write(f"- **{lvl}**: {count} từ ({percent:.1f}%)\n")
            
            # --- PHÂN TÍCH CHỦ ĐỀ ---
            f.write("\n### 2. Phân bổ Chủ đề (Top Topics)\n")
            topic_counts = Counter([d['topic'] for d in group])
            # Sắp xếp các chủ đề theo số lượng giảm dần
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
            
            f.write("| Chủ đề | Số lượng | Tỉ lệ |\n")
            f.write("| :--- | :---: | :---: |\n")
            for topic, count in sorted_topics:
                percent = (count / total * 100) if total > 0 else 0
                f.write(f"| {topic} | {count} | {percent:.1f}% |\n")
            
            f.write("\n" + "-"*40 + "\n\n")

        f.write("---\n")
        f.write("*Báo cáo được thực hiện nhằm tối ưu hóa lộ trình học tập theo chủ đề và trình độ.*")

    print(f"Báo cáo cập nhật đã được xuất tại: {REPORT_FILE}")

if __name__ == "__main__":
    analyze_data()

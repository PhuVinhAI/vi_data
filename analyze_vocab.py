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
    
    # Kiểm tra thư mục words có tồn tại không
    if not os.path.exists(WORDS_DIR):
        print(f"Lỗi: Không tìm thấy thư mục {WORDS_DIR}")
        return

    # Quét tất cả thư mục con trong words
    for folder in os.listdir(WORDS_DIR):
        folder_path = os.path.join(WORDS_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
            
        json_path = os.path.join(folder_path, "data.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    rank = content.get('rank')
                    level = content.get('level', 'N/A')
                    
                    if rank is not None:
                        all_data.append({'rank': rank, 'level': level})
            except Exception as e:
                print(f"Lỗi khi đọc tệp {json_path}: {e}")

    # Sắp xếp theo rank
    all_data.sort(key=lambda x: x['rank'])

    # Các ngưỡng phân tích
    thresholds = [50, 100, 250, 500]
    analysis_results = []

    for t in thresholds:
        # Lọc các từ có rank <= t
        group = [d['level'] for d in all_data if d['rank'] <= t]
        total = len(group)
        counts = Counter(group)
        
        analysis_results.append({
            'threshold': t,
            'total': total,
            'counts': counts
        })

    # Tạo thư mục report nếu chưa có
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    # Ghi file báo cáo Markdown
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Báo cáo Phân tích Trình độ Từ vựng Tiếng Việt\n\n")
        f.write(f"Báo cáo này được tạo dựa trên phân tích dữ liệu từ {len(all_data)} từ vựng.\n\n")
        
        # Danh sách các level để hiển thị theo thứ tự
        target_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'N/A']
        
        for res in analysis_results:
            f.write(f"## Nhóm {res['threshold']} từ đầu tiên (Rank 1-{res['threshold']})\n")
            f.write(f"- **Tổng số từ tìm thấy:** {res['total']}\n")
            
            for lvl in target_levels:
                count = res['counts'].get(lvl, 0)
                # Chỉ hiển thị nếu có dữ liệu hoặc là các bậc cơ bản (để thấy sự thiếu sót)
                if count > 0 or lvl in ['A1', 'A2', 'B1', 'B2']:
                    percent = (count / res['total'] * 100) if res['total'] > 0 else 0
                    f.write(f"  - **{lvl}**: {count} từ ({percent:.1f}%)\n")
            f.write("\n")
            
        f.write("---\n")
        f.write("*Báo cáo được thực hiện tự động nhằm phục vụ công tác kiểm định dữ liệu theo Thông tư 17/2015/TT-BGDĐT.*")

    print(f"Báo cáo đã được xuất thành công tại: {REPORT_FILE}")

if __name__ == "__main__":
    analyze_data()

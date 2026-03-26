import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data\words"

def audit_fields_top_500():
    missing_data = []
    
    for folder in os.listdir(BASE_DIR):
        json_path = os.path.join(BASE_DIR, folder, "data.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('rank', 999) <= 500:
                        issues = []
                        # Kiểm tra các trường bắt buộc
                        if not data.get('exampleSentences') or len(data.get('exampleSentences')) < 3:
                            issues.append("Thiếu ví dụ (cần ít nhất 3)")
                        if not data.get('flashcard', {}).get('definitions', {}).get('vi'):
                            issues.append("Thiếu định nghĩa tiếng Việt")
                        if not data.get('notes') or len(data.get('notes')) < 20:
                            issues.append("Ghi chú quá ngắn hoặc thiếu")
                        if not data.get('topic'):
                            issues.append("Thiếu chủ đề (Topic)")
                        
                        if issues:
                            missing_data.append({
                                'rank': data.get('rank'),
                                'word': data.get('word'),
                                'issues': issues
                            })
            except: pass
            
    missing_data.sort(key=lambda x: x['rank'])
    if not missing_data:
        print("Tất cả 500 từ đầu tiên đều đầy đủ các trường dữ liệu quan trọng.")
    else:
        print(f"Phát hiện {len(missing_data)} từ có vấn đề về dữ liệu:")
        for m in missing_data:
            print(f"Rank {m['rank']:04d} | {m['word']:<15} | Lỗi: {', '.join(m['issues'])}")

if __name__ == "__main__":
    audit_fields_top_500()

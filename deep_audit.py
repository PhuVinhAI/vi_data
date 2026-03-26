import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data\words"

def audit_json_sync():
    # Các trường được coi là "chuẩn" cho một bộ dữ liệu đầy đủ
    REQUIRED_KEYS = [
        'word', 'rank', 'level', 'topic', 'definition', 
        'flashcard', 'exampleSentences', 'exampleSentencesTranslated',
        'notes', 'notes_md', 'multiChoiceQuiz', 'fillBlankQuiz'
    ]
    
    FLASHCARD_KEYS = ['definitions', 'translations', 'example']
    LANGS = ['vi', 'en', 'es']

    results = []
    
    for folder in os.listdir(BASE_DIR):
        json_path = os.path.join(BASE_DIR, folder, "data.json")
        if not os.path.exists(json_path):
            continue
            
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            rank = data.get('rank')
            if rank is None or rank > 500:
                continue
                
            issues = []
            
            # 1. Kiểm tra các trường cấp 1
            for key in REQUIRED_KEYS:
                if key not in data:
                    issues.append(f"Thiếu trường '{key}'")
            
            # 2. Kiểm tra sâu trong flashcard
            fc = data.get('flashcard', {})
            if fc:
                for fkey in FLASHCARD_KEYS:
                    if fkey not in fc:
                        issues.append(f"flashcard: Thiếu '{fkey}'")
                    else:
                        # Kiểm tra ngôn ngữ trong definitions/translations
                        sub_obj = fc.get(fkey, {})
                        for lang in LANGS:
                            if lang not in sub_obj:
                                issues.append(f"flashcard.{fkey}: Thiếu ngôn ngữ '{lang}'")

            # 3. Kiểm tra tính đồng bộ của ví dụ
            exs = data.get('exampleSentences', [])
            ext = data.get('exampleSentencesTranslated', [])
            if len(exs) != len(ext):
                issues.append(f"Số lượng câu ví dụ ({len(exs)}) khác số lượng câu dịch ({len(ext)})")

            if issues:
                results.append({
                    'rank': rank,
                    'word': data.get('word', folder),
                    'issues': issues
                })

        except Exception as e:
            results.append({
                'rank': 999,
                'word': folder,
                'issues': [f"Lỗi đọc tệp: {str(e)}"]
            })

    results.sort(key=lambda x: x['rank'])
    
    if not results:
        print("CHÚC MỪNG: Toàn bộ 500 từ đều đã đồng bộ 100% về cấu trúc JSON.")
    else:
        print(f"PHÁT HIỆN {len(results)} TỪ CHƯA ĐỒNG BỘ CẤU TRÚC:")
        for r in results:
            print(f"Rank {r['rank']:04d} | {r['word']:<15} | Lỗi: {'; '.join(r['issues'])}")

if __name__ == "__main__":
    audit_json_sync()

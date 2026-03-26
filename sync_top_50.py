import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data\words"

# Từ điển bản dịch cơ bản cho Top 50 (vi -> es)
# Chỉ liệt kê một số từ tiêu biểu để làm khung, script sẽ tự nhận diện
ES_MAP = {
    "là": "ser/estar", "cái": "objeto", "có": "tener", "không": "no",
    "và": "y", "trong": "en", "cho": "cho", "với": "con", "đã": "ya/pasado",
    "đang": "estar (gerundio)", "sẽ": "futuro", "về": "sobre/volver",
    "nhưng": "pero", "họ": "ellos", "rồi": "ya", "đến": "venir",
    "lại": "de nuevo", "thấy": "ver", "cám ơn": "gracias", "chị": "hermana"
}

def fix_top_50():
    all_fixed = 0
    for folder in os.listdir(BASE_DIR):
        json_path = os.path.join(BASE_DIR, folder, "data.json")
        if not os.path.exists(json_path): continue
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            rank = data.get('rank', 999)
            if rank > 50: continue
            
            word = data.get('word', "")
            modified = False
            
            # --- 1. Đồng bộ notes_md ---
            if 'notes_md' not in data and 'notes' in data:
                data['notes_md'] = f"**{word}** \n\n {data['notes']}"
                modified = True
                
            # --- 2. Đồng bộ Flashcard ---
            if 'flashcard' not in data:
                # Tạo stub nếu thiếu hẳn flashcard
                data['flashcard'] = {
                    "definitions": {"vi": word, "en": data.get('definition', ""), "es": ""},
                    "translations": {"vi": word, "en": data.get('definition', ""), "es": ""},
                    "example": {"vi": "", "en": "", "es": ""},
                    "audioUrl": "flashcard.mp3"
                }
                modified = True
            
            fc = data['flashcard']
            
            # Bổ sung translations.vi
            if 'translations' in fc:
                if 'vi' not in fc['translations']:
                    fc['translations']['vi'] = word
                    modified = True
                if 'es' not in fc['translations']:
                    fc['translations']['es'] = ES_MAP.get(word, "")
                    modified = True
            
            # Bổ sung definitions.es
            if 'definitions' in fc and 'es' not in fc['definitions']:
                fc['definitions']['es'] = ES_MAP.get(word, "")
                modified = True
                
            # Bổ sung example.es stub
            if 'example' in fc and 'es' not in fc['example']:
                fc['example']['es'] = ""
                modified = True

            if modified:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                all_fixed += 1
                
        except Exception as e:
            print(f"Lỗi tệp {folder}: {e}")

    print(f"Đã đồng bộ thành công {all_fixed} tệp trong Top 50.")

if __name__ == "__main__":
    fix_top_50()

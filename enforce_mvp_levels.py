import os
import json

MVP_DIR = r"c:\Users\tomis\Docs\vi_data\MVP_Top50"

def enforce_mvp_levels():
    updated_count = 0
    # Cấu trúc: {Folder con: Level gán tương ứng}
    LEVEL_MAPPING = {
        "Level_1": "A1",
        "Level_2": "A2"
    }
    
    for level_folder, target_level in LEVEL_MAPPING.items():
        level_path = os.path.join(MVP_DIR, level_folder)
        if not os.path.exists(level_path): continue
        
        # Duyệt qua các chủ đề và thư mục từ
        for root, dirs, files in os.walk(level_path):
            if "data.json" in files:
                json_path = os.path.join(root, "data.json")
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Cập nhật level nếu khác với target_level
                if data.get('level') != target_level:
                    data['level'] = target_level
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    updated_count += 1

    print(f"THÀNH CÔNG: Đã áp mã trình độ (A1/A2) cho {updated_count} tệp dữ liệu!")

if __name__ == "__main__":
    enforce_mvp_levels()

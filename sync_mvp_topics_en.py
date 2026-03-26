import os
import json

MVP_DIR = r"c:\Users\tomis\Docs\vi_data\MVP_Top50"

# Map thư mục sang tên chủ đề tiếng ANH chuẩn
TOPIC_NAME_MAP_EN = {
    "Topic_1_Pronouns": "Pronouns & Titles",
    "Topic_2_States_Ownership": "States & Ownership",
    "Topic_3_Basic_Actions": "Basic Actions",
    "Topic_4_Time_Connectors": "Time & Connectors"
}

def sync_mvp_topics_en():
    updated_count = 0
    
    for level_folder in os.listdir(MVP_DIR):
        level_path = os.path.join(MVP_DIR, level_folder)
        if not os.path.isdir(level_path): continue
        
        for topic_folder in os.listdir(level_path):
            topic_path = os.path.join(level_path, topic_folder)
            if not os.path.isdir(topic_path): continue
            
            # Lấy tên tiếng ANH từ map
            target_topic_name = TOPIC_NAME_MAP_EN.get(topic_folder, "Other")
            
            for word_folder in os.listdir(topic_path):
                word_path = os.path.join(topic_path, word_folder)
                json_path = os.path.join(word_path, "data.json")
                
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Cập nhật topic sang tiếng Anh
                    if data.get('topic') != target_topic_name:
                        data['topic'] = target_topic_name
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        updated_count += 1

    print(f"THÀNH CÔNG: Đã đồng bộ tên Chủ đề bằng tiếng ANH cho {updated_count} tệp dữ liệu!")

if __name__ == "__main__":
    sync_mvp_topics_en()

import os
import shutil

# Đường dẫn nguồn và đích
SOURCE_DIR = r"c:\Users\tomis\Docs\vi_data\words"
MVP_DIR = r"c:\Users\tomis\Docs\vi_data\MVP_Top50"

# Cấu trúc quy hoạch MVP
MVP_STRUCTURE = {
    "Level_1": {
        "Topic_1_Pronouns": ["0003", "0007", "0014", "0029", "0031", "0034", "0037", "0044"],
        "Topic_2_States_Ownership": ["0001", "0002", "0005", "0008", "0009", "0010", "0011", "0013", "0025", "0026", "0027"],
        "Topic_3_Basic_Actions": ["0024", "0033", "0041", "0043", "0048", "0049", "0050"]
    },
    "Level_2": {
        "Topic_4_Time_Connectors": [
            "0004", "0006", "0012", "0015", "0016", "0017", "0018", "0019", "0020", "0021", 
            "0022", "0023", "0028", "0030", "0032", "0035", "0036", "0038", "0039", "0040", 
            "0042", "0045", "0046", "0047"
        ]
    }
}

def organize_mvp():
    # Lấy danh sách tất cả các folder từ vựng hiện có
    source_folders = os.listdir(SOURCE_DIR)
    words_copied = 0

    # Duyệt qua cấu trúc MVP để tạo folder và copy
    for level, topics in MVP_STRUCTURE.items():
        for topic, ids in topics.items():
            target_path = os.path.join(MVP_DIR, level, topic)
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            
            for word_id in ids:
                # Tìm folder nguồn khớp với ID (ví dụ '0001_là' khớp với ID '0001')
                found_folder = next((f for f in source_folders if f.startswith(word_id)), None)
                
                if found_folder:
                    src_path = os.path.join(SOURCE_DIR, found_folder)
                    dst_path = os.path.join(target_path, found_folder)
                    
                    # Copy nguyên folder (bao gồm data.json và assets nếu có)
                    if os.path.exists(dst_path):
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                    words_copied += 1
                else:
                    print(f"CẢNH BÁO: Không tìm thấy folder cho ID {word_id}")

    print(f"HOÀN TẤT: Đã quy hoạch xong {words_copied}/50 từ vào thư mục {MVP_DIR}")

if __name__ == "__main__":
    organize_mvp()

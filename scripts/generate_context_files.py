import os
import math

def generate_context_files_by_rank(words_dir, output_dir, range_size=100):
    # Lấy danh sách các thư mục trong words/
    folders = [f for f in os.listdir(words_dir) if os.path.isdir(os.path.join(words_dir, f))]
    folders.sort() # Đảm bảo sắp xếp đúng thứ tự
    
    # Tạo một dictionary để gom nhóm theo dải rank
    groups = {}

    for folder in folders:
        try:
            rank = int(folder.split('_')[0])
            group_idx = (rank - 1) // range_size
            if group_idx not in groups:
                groups[group_idx] = []
            groups[group_idx].append(folder)
        except (ValueError, IndexError):
            continue

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_lines = []

    # Xuất các file theo từng nhóm đã gom
    for group_idx in sorted(groups.keys()):
        chunk = sorted(groups[group_idx])
        
        start_r = group_idx * range_size + 1
        end_r = (group_idx + 1) * range_size
        
        file_name = f"context_{start_r:04d}_{end_r:04d}.txt"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for folder in chunk:
                line = f"{folder}/data.json\n"
                f.write(line)
                all_lines.append(line)
        
        print(f"Đã tạo: {file_name} ({len(chunk)} từ)")

    # Gộp tất cả vào một file duy nhất
    all_file_path = os.path.join(output_dir, "context_all.txt")
    with open(all_file_path, 'w', encoding='utf-8') as f:
        f.writelines(all_lines)
    print(f"Đã tạo file gộp: context_all.txt ({len(all_lines)} từ)")

if __name__ == "__main__":
    base_path = r"c:\Users\tomis\Docs\vi_data"
    words_path = os.path.join(base_path, "words")
    output_path = os.path.join(base_path, "contexts")
    
    if os.path.exists(output_path):
        import shutil
        shutil.rmtree(output_path)
    
    generate_context_files_by_rank(words_path, output_path)

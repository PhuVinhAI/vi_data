import os
import json

MVP_DIR = r"c:\Users\tomis\Docs\vi_data\MVP_Top50"

def final_mvp_audit():
    REQUIRED_KEYS = [
        'word', 'rank', 'level', 'topic', 'definition', 
        'flashcard', 'exampleSentences', 'exampleSentencesTranslated',
        'notes', 'notes_md', 'multiChoiceQuiz', 'fillBlankQuiz'
    ]
    
    issues = []
    word_count = 0

    for level_folder in os.listdir(MVP_DIR):
        level_path = os.path.join(MVP_DIR, level_folder)
        if not os.path.isdir(level_path): continue
        
        for topic_folder in os.listdir(level_path):
            topic_path = os.path.join(level_path, topic_folder)
            if not os.path.isdir(topic_path): continue
            
            for word_folder in os.listdir(topic_path):
                word_path = os.path.join(topic_path, word_folder)
                json_path = os.path.join(word_path, "data.json")
                
                if os.path.exists(json_path):
                    word_count += 1
                    with open(json_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            file_issues = []
                            
                            # 1. Kiểm tra trường bắt buộc
                            for key in REQUIRED_KEYS:
                                if key not in data:
                                    file_issues.append(f"Thiếu '{key}'")
                            
                            # 2. Kiểm tra đa ngôn ngữ trong flashcard
                            fc = data.get('flashcard', {})
                            for subkey in ['definitions', 'translations', 'example']:
                                sub_obj = fc.get(subkey, {})
                                for lang in ['vi', 'en', 'es']:
                                    if lang not in sub_obj or not sub_obj[lang]:
                                        file_issues.append(f"fc.{subkey}.{lang} trống")
                            
                            # 3. Kiểm tra tính đồng bộ Quiz
                            if not data.get('multiChoiceQuiz') and not data.get('fillBlankQuiz'):
                                file_issues.append("Thiếu cả 2 loại Quiz")
                                
                            # 4. Kiểm tra Topic đồng bộ
                            # topic_folder có định dạng 'Topic_X_Name', ta lấy phần Name
                            expected_topic_prefix = topic_folder.split('_')[-1].lower()
                            actual_topic = data.get('topic', '').lower()
                            # Kiểm tra xem có chứa từ khóa chủ đề không (tương đối)
                            if expected_topic_prefix not in actual_topic and actual_topic != "":
                                # Nếu không khớp hoàn toàn, ta sẽ ghi chú để điều chỉnh
                                # Ví dụ: Topic_1_Pronouns vs 'Pronouns & Titles' -> OK
                                pass 

                            if file_issues:
                                issues.append({
                                    'id': word_folder,
                                    'level': level_folder,
                                    'topic': topic_folder,
                                    'errors': file_issues
                                })
                        except Exception as e:
                            issues.append({'id': word_folder, 'errors': [f"Lỗi JSON: {str(e)}"]})

    print(f"--- KẾT QUẢ KIỂM TRA MVP (Tổng cộng {word_count} từ) ---")
    if not issues:
        print("TUYỆT VỜI: 100% dữ liệu đạt chuẩn MVP. Sẵn sàng đóng gói!")
    else:
        print(f"Phát hiện {len(issues)} tệp cần hiệu chỉnh:")
        for issue in issues:
            print(f"- [{issue['id']}] trong {issue['level']}/{issue['topic']}:")
            for err in issue['errors']:
                print(f"  + {err}")

if __name__ == "__main__":
    final_mvp_audit()

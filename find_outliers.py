import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data"
WORDS_DIR = os.path.join(BASE_DIR, "words")

def find_outliers():
    outliers = []
    topic_distribution = {}
    
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
                    topic = content.get('topic', 'N/A')
                    word = content.get('word', folder)
                    
                    if rank is not None and rank <= 500:
                        # Theo dõi phân bổ chủ đề
                        topic_distribution[topic] = topic_distribution.get(topic, 0) + 1
                        
                        # Tìm các từ có trình độ B2, C1, C2
                        if level in ['B2', 'C1', 'C2']:
                            outliers.append({
                                'word': word,
                                'rank': rank,
                                'level': level,
                                'topic': topic,
                                'path': json_path
                            })
            except Exception:
                continue

    # Sắp xếp outliers theo rank
    outliers.sort(key=lambda x: x['rank'])
    
    print("--- DANH SÁCH TỪ CÓ TRÌNH ĐỘ CAO TRONG TOP 500 ---")
    for o in outliers:
        print(f"Rank {o['rank']:04d} | Từ: {o['word']:<15} | Level: {o['level']} | Topic: {o['topic']}")
        
    print("\n--- PHÂN BỔ CHỦ ĐỀ TRONG TOP 500 ---")
    sorted_topics = sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True)
    for topic, count in sorted_topics:
        print(f"{topic:<25}: {count} từ")

if __name__ == "__main__":
    find_outliers()

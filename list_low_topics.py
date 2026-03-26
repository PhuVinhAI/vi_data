import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data\words"
TARGET_TOPICS = [
    'Animals & Nature', 'Society & Events', 'Culture & Beliefs', 
    'Culture & Traditions', 'Language & Communication', 'Daily Life & Services'
]

def list_low_count_topics():
    results = []
    for folder in os.listdir(BASE_DIR):
        json_path = os.path.join(BASE_DIR, folder, "data.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('rank', 999) <= 500 and data.get('topic') in TARGET_TOPICS:
                        results.append({
                            'rank': data.get('rank'),
                            'word': data.get('word'),
                            'topic': data.get('topic')
                        })
            except: pass
            
    results.sort(key=lambda x: x['rank'])
    for r in results:
        print(f"Rank {r['rank']:04d} | {r['word']:<15} | Topic: {r['topic']}")

if __name__ == "__main__":
    list_low_count_topics()

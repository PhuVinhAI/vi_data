import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data\words"

def list_abstract_top_500():
    results = []
    for folder in os.listdir(BASE_DIR):
        json_path = os.path.join(BASE_DIR, folder, "data.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('rank', 999) <= 500 and data.get('topic') == 'Abstract Concepts':
                        results.append({
                            'rank': data.get('rank'),
                            'word': data.get('word'),
                            'level': data.get('level')
                        })
            except: pass
            
    results.sort(key=lambda x: x['rank'])
    for r in results:
        print(f"{r['rank']:04d} | {r['word']:<15} | {r['level']}")

if __name__ == "__main__":
    list_abstract_top_500()

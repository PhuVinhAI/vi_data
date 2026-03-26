import os
import json

BASE_DIR = r"c:\Users\tomis\Docs\vi_data\words"

def audit_top_50():
    REQUIRED_KEYS = [
        'word', 'rank', 'level', 'topic', 'definition', 
        'flashcard', 'exampleSentences', 'exampleSentencesTranslated',
        'notes', 'notes_md', 'multiChoiceQuiz', 'fillBlankQuiz'
    ]
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
            if rank is None or rank > 50:
                continue
                
            issues = []
            for key in REQUIRED_KEYS:
                if key not in data:
                    issues.append(f"Thiếu '{key}'")
            
            fc = data.get('flashcard', {})
            if fc:
                for fkey in ['definitions', 'translations', 'example']:
                    if fkey not in fc:
                        issues.append(f"flashcard: Thiếu '{fkey}'")
                    else:
                        sub_obj = fc.get(fkey, {})
                        for lang in LANGS:
                            if lang not in sub_obj:
                                issues.append(f"fc.{fkey}.{lang}")

            if issues:
                results.append({'rank': rank, 'word': data.get('word', folder), 'issues': issues})
        except: pass

    results.sort(key=lambda x: x['rank'])
    for r in results:
        print(f"Rank {r['rank']:02d} | {r['word']:<10} | Lỗi: {', '.join(r['issues'])}")

if __name__ == "__main__":
    audit_top_50()

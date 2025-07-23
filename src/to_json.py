import json
from pathlib import Path

source = [
    ('clean/passage.txt', 'passage'),
    ('clean/author_info.txt', 'author_info'),
    ('clean/cleaned_questions_fixed.txt', 'questions'),
    ('clean/word_meaning.txt', 'word_meaning')
]

def to_json(source):
    data = []

    for path, doc_type in source:
        path = Path(path)

        with path.open('r', encoding='utf-8') as f:
            text = f.read().strip()

        entry = {
            'type': doc_type,
            'text': text
        }

        data.append(entry)

    with open('clean/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

to_json(source)

        
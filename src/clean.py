import re

def clean_text(text: str) -> str:
    text = text.strip()
    # Remove weird non-Bangla/non-English characters
    text = re.sub(r'[^\u0980-\u09FF0-9A-Za-z.,?!()\s:\-\'\"—]', '', text)
    # Normalize multiple newlines and spaces
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_passage_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Split by page or manually if needed
    cleaned = clean_text(raw)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

def clean_word_meaning_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = [clean_text(line) for line in lines if line.strip()]
    
    with open(output_path, "w", encoding="utf-8") as f:
        for line in cleaned_lines:
            f.write(line + "\n")


clean_passage_file('data/questions.txt', 'clean/questions.txt')
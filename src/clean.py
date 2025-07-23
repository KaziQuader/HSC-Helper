import re
from pathlib import Path

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

# def clean_questions(text: str) -> str:
#     # Replace non-breaking spaces and normalize whitespace
#     text = text.replace('\u00a0', ' ')
#     text = re.sub(r'[ \t]+', ' ', text)

#     # Collapse multiple newlines
#     text = re.sub(r'\n{2,}', '\n', text)

#     # Ensure each numbered question (e.g., ১। or ১:) starts on a new line
#     text = re.sub(r'(?<!\n)([০-৯]+[।:\)])', r'\n\1', text)

#     # Clean stray whitespace
#     lines = [line.strip() for line in text.splitlines()]
#     return '\n'.join(lines).strip()

def clean_questions(text: str) -> str:
    # Fix broken Bangla digits split across lines
    text = fix_broken_bangla_numbers(text)

    # Replace non-breaking spaces and normalize whitespace
    text = text.replace('\u00a0', ' ')
    text = re.sub(r'[ \t]+', ' ', text)

    # Collapse multiple newlines
    text = re.sub(r'\n{2,}', '\n', text)

    # Ensure numbered questions start on a new line
    text = re.sub(r'(?<!\n)([০-৯]+[।:\)])', r'\n\1', text)

    # Strip excess whitespace
    lines = [line.strip() for line in text.splitlines()]
    return '\n'.join(lines).strip()


def fix_broken_bangla_numbers(text: str) -> str:
    # Join broken bangla numbers like "৪\n৭" => "৪৭"
    text = re.sub(r'([০-৯])\n([০-৯])', r'\1\2', text)
    return text

# questions_path = Path("data/questions.txt")
# output_path = Path("clean/questions_cleaned_1.txt")

# raw_questions = questions_path.read_text(encoding="utf-8")
# cleaned_questions = clean_questions(raw_questions)
# output_path.write_text(cleaned_questions, encoding="utf-8")

import re

def merge_split_bangla_numbers(text: str) -> str:
    lines = text.splitlines()
    merged_lines = []

    i = 0
    while i < len(lines):
        # Check if line has a single Bangla digit
        if re.fullmatch(r'[০-৯]', lines[i].strip()) and i + 1 < len(lines):
            # Merge with the next line
            merged = lines[i].strip() + lines[i + 1].strip()
            merged_lines.append(merged)
            i += 2  # skip the next line
        else:
            merged_lines.append(lines[i])
            i += 1

    return '\n'.join(merged_lines)

with open("clean/questions_cleaned.txt", "r", encoding="utf-8") as f:
    cleaned = f.read()

fixed = merge_split_bangla_numbers(cleaned)

with open("clean/cleaned_questions_fixed.txt", "w", encoding="utf-8") as f:
    f.write(fixed)
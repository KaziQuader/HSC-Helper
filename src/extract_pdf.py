from pdf2image import convert_from_path
import pytesseract

class Extractor:
    def __init__(self, path, output_path):
        self.path = path
        self.output_path = output_path

    def extract(self):
        pages = convert_from_path(self.path, dpi=600)
        full_text = ''

        for i, page in enumerate(pages):
            text = pytesseract.image_to_string(page, lang="ben")
            full_text += f"--- Page {i+1} ---\n{text}\n"

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

    
              
passage_path = 'data/passage.pdf'
author_path = 'data/author_info.pdf'
word_meaning_path = 'data/word_meaning.pdf'
questions = 'data/questions.pdf'

Extractor(word_meaning_path, 'data/word_meaning.txt').extract()



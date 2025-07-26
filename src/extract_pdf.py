from pdf2image import convert_from_path
import pytesseract
import re
import unicodedata
from dotenv import load_dotenv
import os

# load_dotenv()
# tessdata_path = os.getenv('TESSDATA_PREFIX')
# poppler_path = os.getenv('POPPLER_PATH')
class ExtractPDF:
    def __init__(self, path, output_path):
        self.path = path
        self.output_path = output_path

    def clean_text(self, text):
        # Remove page numbers (lines that are just numbers)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        # Remove common headers/footers (customize as needed)
        text = re.sub(r'^.*(HSC.*Bangla.*Paper).*\n?', '', text, flags=re.MULTILINE | re.IGNORECASE)
        # Normalize unicode (for Bangla/English)
        text = unicodedata.normalize("NFKC", text)
        # Remove multiple consecutive newlines
        text = re.sub(r'\n+', '\n', text)
        # Remove excessive spaces
        text = re.sub(r'[ \t]+', ' ', text)
        # Remove page numbers like "পৃষ্ঠা ১২" or "Page 12"
        text = re.sub(r"(পৃষ্ঠা|Page)\s*\d+", "", text)
        # Remove mixed digit lines (e.g., phone numbers, batch codes)
        text = re.sub(r"(?:(?:\d|[০-৯])\s*){5,}", "", text)
        # # Remove lines that are mostly garbage (digits, symbols, random OCR mistakes)
        text = re.sub(r"^[^\u0980-\u09FF]{4,}.*$", "", text, flags=re.MULTILINE)
        # # Remove excess newlines and collapse spaces
        text = re.sub(r"\s+", " ", text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text

    def extract_text(self):
        pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

        print("Converting Pages to Images")
        pages = convert_from_path(self.path, dpi=600)
        full_text = ''

        print("Extracting Text from Images")
        for i, page in enumerate(pages):
            text = pytesseract.image_to_string(page, lang="ben")
            text = self.clean_text(text)
            full_text += text+ "\n"

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print("Written to the folder clean/")
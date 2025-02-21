import fitz  # PyMuPDF
import re

def clean_text(text):
    # Убираем специальные символы и заменяем множественные пробелы на один
    cleaned_text = re.sub(r'\s+', ' ', text)
    # Убираем не алфавитные символы, если это нужно
    # cleaned_text = re.sub(r'[^а-яА-Яa-zA-Z0-9,.!? ]', '', cleaned_text)
    return cleaned_text.strip()


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text
#
# pdf_path = "../src/first.pdf"
# text = extract_text_from_pdf(pdf_path)
# print(text[:500])  # Пример первых 500 символов текста
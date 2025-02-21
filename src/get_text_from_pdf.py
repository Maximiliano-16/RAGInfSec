import fitz  # PyMuPDF

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
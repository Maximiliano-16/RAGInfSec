from dotenv import load_dotenv

from src import get_text_from_pdf
import os

# Загружаем переменные из .env
load_dotenv()

# Получаем путь до папки
pdf_folder_path = os.getenv("PDF_FOLDER_PATH")

print(f"Путь до папки: {pdf_folder_path}")


def main():
    for filename in os.listdir(pdf_folder_path):
        # Проверяем, что файл имеет расширение .pdf
        if filename.endswith(".pdf"):
            # Получаем полный путь до файла
            file_path = os.path.join(pdf_folder_path, filename)
            # Вызываем функцию для обработки PDF-файла
            text = get_text_from_pdf.extract_text_from_pdf(file_path)
            print(text[:500])
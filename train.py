from dotenv import load_dotenv
import src.get_text_from_pdf as gpdf

from src import get_text_from_pdf
import os

# Загружаем переменные из .env
load_dotenv()

# Получаем путь до папки
pdf_folder_path = os.getenv("PDF_FOLDER_PATH")

print(f"Путь до папки: {pdf_folder_path}")


def main():
    texts = ''
    for filename in os.listdir(pdf_folder_path):
        # Проверяем, что файл имеет расширение .pdf
        if filename.endswith(".pdf"):
            # Получаем полный путь до файла
            file_path = os.path.join(pdf_folder_path, filename)
            # Вызываем функцию для обработки PDF-файла
            texts += gpdf.extract_text_from_pdf(file_path)
            print(texts[:500])
            
    cleaned_text = gpdf.clean_text(texts)



if __name__ == '__main__':
    main()
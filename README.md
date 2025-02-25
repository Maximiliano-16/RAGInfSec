# RAGInfSec: Retrieval-Augmented Generation System for Information Security

RAGInfSec – это система, основанная на принципе Retrieval-Augmented Generation (RAG), которая позволяет отвечать на вопросы по информационной безопасности, используя тексты из PDF-документов.  

Проект использует FAISS для быстрого поиска по векторному пространству, HuggingFace embeddings для преобразования текста и модель GigaChat для генерации ответов.  

API, построенное с FastAPI, обеспечивает удобный интерфейс для отправки запросов.  

## Особенности

- **Извлечение текста из PDF:** Парсинг и очистка документов для дальнейшей обработки.
- **Разбиение и индексация текста:** Разбиение на чанки и создание векторного индекса с помощью FAISS.
- **Retrieval-Augmented Generation:** Генерация ответов на основе извлечённого контекста с помощью GigaChat.
- **API на FastAPI:** Возможность отправлять запросы и получать ответы через REST API.

## Установка и настройка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/your_username/RAGInfSec.git
   cd RAGInfSec

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   # На Windows:
   venv\Scripts\activate
   # На Unix/Mac:
   source venv/bin/activate
   
3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt

4. **Настройте переменные окружения:**
Создайте файл .env в корневой директории проекта и укажите необходимые переменные, например:

   ```dotenv
   PDF_FOLDER_PATH=path/to/your/pdf/folder
   MY_SECRET_TOKEN=your_gigachat_token

## Структура проекта

    RAGInfSec/
    ├── data/                # Данные для обучения и тестирования
    ├── models/              # Предобученные модели
    ├── src/                 # Исходный код проекта
    ├── config/              # Файлы конфигураций
    ├── notebooks/           # Jupyter Notebooks для экспериментов
    ├── requirements.txt     # Зависимости проекта
    └── README.md            # Описание проекта

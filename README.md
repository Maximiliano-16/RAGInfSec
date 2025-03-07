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

## Использование
1. **Построение индекса**
Сначала запустите скрипт для построения векторного индекса из PDF-документов:

   ```
   python build_index.py
   
Это создаст папку faiss_index/, в которой будет храниться индекс для дальнейшего использования.

2. **Запуск API-сервера**
Запустите API-сервер с помощью uvicorn:

   ```bash
   uvicorn app.main:app --reload
   
API будет доступно по адресу http://127.0.0.1:8000.

3. **Отправка запросов**
Отправьте POST-запрос к эндпоинту /ask. Пример с использованием curl:

   ```bash
   curl -X POST "http://127.0.0.1:8000/ask" \
        -H "Content-Type: application/json" \
        -d '{"question": "Какие уровни в обеспечении информационной безопасности можно выделить?"}'

Или воспользуйтесь Postman для отправки запроса с JSON-объектом:

   ```json
   {
   "question": "Какие уровни в обеспечении информационной безопасности можно выделить?"
   }
   ```
Ответ также придёт JSON-объектом с ключём answer

## Структура проекта

    RAGInfSec/
    ├── data/                # Папка с презентациями в формате PDF
    ├── app/                 # Папка с созданием REST API
    ├── src/                 # Папка с функциям по работе с данными 
    ├── config/              # Файлы конфигураций
    ├── notebooks/           # Jupyter Notebooks для экспериментов
    ├── build_index.py       # Файл создания FAISS индекса
    ├── ask_question.py      # Файл для тестирования вопросов-ответов
    ├── requirements.txt     # Зависимости проекта
    └── README.md            # Описание проекта

## Используемые технологии

- **Python** – основной язык разработки.
- **FastAPI** – для создания REST API.
- **Uvicorn** – ASGI-сервер для запуска FastAPI-приложения.
- **FAISS** – библиотека для векторного поиска.
- **HuggingFace Embeddings & Sentence Transformers** – для преобразования текста в эмбеддинги.
- **GigaChat & GigaChain** – для генерации ответов.
- **PyMuPDF** – для извлечения текста из PDF.
- **python-dotenv** – для работы с переменными окружения.

## Заключение
В рамках проекта удалось:
 - Создать систему для извлечения, индексирования и обработки текстовой информации из PDF-документов.
 - Реализовать быстрый поиск по текстовому контексту с использованием FAISS.
 - Объединить поиск и генерацию ответов с помощью Retrieval-Augmented Generation.
 - Разработать REST API для удобного доступа к системе, что позволяет интегрировать проект в различные приложения.  
Этот проект демонстрирует применение современных технологий для решения задачи извлечения знаний из неструктурированных данных и генерации информативных ответов.



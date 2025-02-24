import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from dotenv import load_dotenv
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Импорт зависимостей для LangChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import GigaChat

# Инициализация FastAPI
app = FastAPI(title="RAG API для Информационной безопасности ")

# Инициализация embeddings
model_name = "distilbert-base-nli-mean-tokens"
embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

# Загрузка сохранённого индекса FAISS
vector_store = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
# try:
#     vector_store = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
# except Exception as e:
#     raise HTTPException(status_code=500, detail=f"Ошибка загрузки векторного индекса: {e}")

embedding_retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Инициализация LLM
my_credentials = os.getenv("MY_SECRET_TOKEN")
llm = GigaChat(credentials=my_credentials,
               model='GigaChat:latest',
               verify_ssl_certs=False,
               profanity_check=False)

# Создание шаблона для промпта
prompt = ChatPromptTemplate.from_template(
    '''Ответь на вопрос пользователя. Используй при этом только информацию из контекста. 
Контекст: {context}
Вопрос: {input}
Ответ:'''
)

# Создание цепочки для комбинирования документов и генерации ответа
document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)

retrieval_chain = create_retrieval_chain(embedding_retriever, document_chain)

# Описание модели данных для запроса и ответа
class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

# Эндпоинт для получения ответа на вопрос
@app.post("/ask", response_model=Answer)
def ask_question(q: Question):
    response = retrieval_chain.invoke({'input': q.question})
    answer_text = response.get('answer', '')
    return Answer(answer=answer_text)

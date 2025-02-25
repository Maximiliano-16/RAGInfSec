from langchain_community.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import GigaChat
from dotenv import load_dotenv
import os

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings



# Загружаем переменные из .env
load_dotenv()

# Получаем путь до папки
pdf_folder_path = os.getenv("PDF_FOLDER_PATH")
my_credentials = os.getenv("MY_SECRET_TOKEN")

# Параметры модели и embeddings
model_name = "distilbert-base-nli-mean-tokens"
embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

# Загружаем сохраненный индекс
vector_store = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

embedding_retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Настройка LLM и цепочки
llm = GigaChat(credentials=my_credentials,
               model='GigaChat:latest',
               verify_ssl_certs=False,
               profanity_check=False)

prompt = ChatPromptTemplate.from_template('''Ответь на вопрос пользователя. \
    Используй при этом только информацию из контекста. 
    Контекст пердставляет собой информацию из обучающих презентаций по информационной безопасности
    Если в контексте нет информации для ответа, сообщи об этом пользователю и сгенерируй общий ответ.
    Контекст: {context}
    Вопрос: {input}
    Ответ:''')

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)

retrieval_chain = create_retrieval_chain(embedding_retriever, document_chain)

# Пример запроса
question = "Какие уровни в обеспечении информационой безопасности можно выделить?"
response = retrieval_chain.invoke({'input': question})
print(response['answer'])

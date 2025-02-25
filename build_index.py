from dotenv import load_dotenv
import src.get_text_from_pdf as gpdf
import src.create_dock_store as cds

from langchain_community.llms import GigaChat
from langchain_community.vectorstores import FAISS
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings




from src import get_text_from_pdf

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"



# Загружаем переменные из .env
load_dotenv()

# Получаем путь до папки
pdf_folder_path = os.getenv("PDF_FOLDER_PATH")
my_credentials = os.getenv("MY_SECRET_TOKEN")

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
    chunks = cds.split_text_into_chunks(cleaned_text)
    dock_store = cds.create_docstore(chunks)

    print(len(dock_store))
    print(dock_store[1])

    llm = GigaChat(credentials=my_credentials,
                   model='GigaChat:latest',
                   verify_ssl_certs=False,
                   profanity_check=False)

    # model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    model_name = "distilbert-base-nli-mean-tokens"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}

    embedding = HuggingFaceEmbeddings(model_name=model_name,
                                      model_kwargs=model_kwargs,
                                      encode_kwargs=encode_kwargs)
    # print('------------------------')


    vector_store = FAISS.from_documents(dock_store, embedding=embedding)

    vector_store.save_local("faiss_index")
    print("Индекс успешно сохранён")

    # embedding_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    # prompt = ChatPromptTemplate.from_template('''Ответь на вопрос пользователя. \
    # Используй при этом только информацию из контекста.
    # Контекст пердставляет собой информацию из обучающих презентаций по информационной безопасности
    # Если в контексте нет информации для ответа, сообщи об этом пользователю.
    # Контекст: {context}
    # Вопрос: {input}
    # Ответ:''')
    # document_chain = create_stuff_documents_chain(
    #     llm=llm,
    #     prompt=prompt
    # )
    # retrieval_chain = create_retrieval_chain(embedding_retriever,
    #                                          document_chain)
    #
    # q1 = 'какие существуют основные атаки в сети интернет?'
    #
    # resp1 = retrieval_chain.invoke(
    #     {'input': q1}
    # )
    # print(resp1['answer'])
    #
    # q2 = 'Какие уровни в обеспечении информационой безопасности можно выделить?'
    #
    # resp2 = retrieval_chain.invoke(
    #     {'input': q2}
    # )
    # print(resp2['answer'])

    # from langchain_core.messages import HumanMessage
    #
    # response = llm.invoke([HumanMessage(content="Привет, ты кто?")])
    # print(response)



if __name__ == '__main__':
    main()
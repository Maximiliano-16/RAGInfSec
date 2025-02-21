def create_docstore(chunks):
    # Создаем хранилище документов с метаданными
    from langchain.docstore import InMemoryDocstore
    from langchain.schema import Document

    docs = [
        Document(
            page_content=text,
            metadata={'source': f'doc_{i}'}
        ) for i, text in enumerate(chunks)
    ]
    # return InMemoryDocstore(
    #     {str(i): doc for i, doc in enumerate(docs)}
    # )
    return docs

def split_text_into_chunks(text, chunk_size=500):
    # Разбиваем текст по предложениям или абзацам
    chunks = []
    sentences = text.split('. ')
    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence)
        if len(' '.join(current_chunk)) > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks



# chunks = split_text_into_chunks(cleaned_text)
# print(f"Количество фрагментов: {len(chunks)}")
# print(chunks[:2])  # Пример первых двух фрагментов
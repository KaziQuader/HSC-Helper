from langchain.text_splitter import RecursiveCharacterTextSplitter
from extract_pdf import ExtractPDF
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_community.vectorstores import Qdrant
import os

def get_text_chunks_from_lines(lines, chunk_size=1024, chunk_overlap=200):
    full_text = "\n".join(lines)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "।", "?", "!"]  # Bengali + English-aware
    )

    return splitter.split_text(full_text)

def data_pipeline(input_path, output_path):
    if not os.path.exists("clean/full_text.txt"):
        extractor = ExtractPDF(input_path, output_path)
        extractor.extract_text()

    file_path = Path(output_path)
    with file_path.open(encoding="utf-8") as f:
        lines = f.read().splitlines() 
    chunks = get_text_chunks_from_lines(lines)

    documents = [Document(page_content=chunk) for chunk in chunks]

    for doc in documents[:5]:
        print(doc)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


    return documents, embedding_model

def create_vector_db(input_path, output_path, url="http://localhost:6333", collection_name='hsc_helper'):
    documents, embedding_model = data_pipeline(input_path, output_path)

    qdrant = QdrantClient(url=url)

    if collection_name not in [col.name for col in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    # # Store in Qdrant
    # vectorstore = Qdrant.from_documents(
    #     documents=documents,
    #     embedding=embedding_model,
    #     client=qdrant,
    #     collection_name=collection_name,
    # )
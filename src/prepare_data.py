from langchain.text_splitter import RecursiveCharacterTextSplitter
from extract_pdf import ExtractPDF
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import os
import uuid

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

    embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    embedding_dim = embedding_model.get_sentence_embedding_dimension()
    embeddings = embedding_model.encode(chunks)

    payload = [{"text": chunk} for chunk in chunks]

    return payload, embeddings, embedding_dim

def create_vector_db(input_path, output_path, url="http://localhost:6333", collection_name='hsc_helper'):
    qdrant = QdrantClient(url)

    payload, embeddings, embedding_dim = data_pipeline(input_path, output_path)

    if collection_name not in [col.name for col in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
            )
        )

    points = [PointStruct(id=str(uuid.uuid4()), vector=embeddings.tolist(), payload=payload) for embeddings, payload in zip(embeddings, payload)]
    qdrant.upsert(collection_name=collection_name, points=points)
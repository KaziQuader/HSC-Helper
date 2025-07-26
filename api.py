from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from collections import deque
from typing import Dict
import os
from contextlib import asynccontextmanager
from src.prepare_data import create_vector_db
from src.rag import generate
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

qdrant = None
collection_name = None
embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
agent = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.15)
chat_histories: Dict[str, deque] = {}

class GenerateRequest(BaseModel):
    session_id: str
    query: str

# Creates the VectorDB at initial startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global qdrant, collection_name
    print("🔄 Loading Vector DB...")
    qdrant, collection_name = create_vector_db(
        'data/HSC26-Bangla1st-Paper.pdf',
        'clean/full_text.txt',
        embedding_model
    )
    print("✅ Vector DB loaded.")
    yield
    print("🧹 Cleanup if needed.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "RAG API is running ✅"}


@app.post('/generate')
async def generate_response(req: GenerateRequest):
    session_id = req.session_id
    query = req.query

    if session_id not in chat_histories:
        chat_histories[session_id] = deque(maxlen=10)
    memory = chat_histories[session_id]
    chat_history = None

    response, chat_history = generate(
        query,
        agent,
        embedding_model,
        chat_history,
        memory,
        qdrant,
        collection_name
    )

    return JSONResponse({
        'session_id' :session_id,
        'query': query,
        'response': response,
        'memory': list(memory),
        'chat_history': chat_history
    })

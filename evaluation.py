from sentence_transformers import SentenceTransformer, util
from qdrant_client import QdrantClient
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from src.rag import retrieve
from src.prompt_template import generate_prompt_template

evaluation_dataset = [
    {
        "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
        "expected_context_keywords": ["কল্যাণী", "বয়স", "বিয়ে"],
        "expected_answer": "পনেরো"
    },
    {
        "query": "অনুপমের বাবার পেশা কী ছিল?",
        "expected_context_keywords": ["অনুপম", "বাবা", "ওকালতি"],
        "expected_answer": "ওকালতি"
    },
    {
        'query': "কল্যানীর বাবার নাম কী ছিল?",
        'expected_context_keywords': ["কল্যাণী","বাবা", "নাম"],
        'expected_answer': "শম্ভুনাথ বাবু"
    },
    {
        'query': "অপরিচিতা গল্পে কল্যানীর বিয়ে না হওয়ার কারন কী ছিল?",
        'expected_context_keywords': ["কল্যাণী", "না", "বিয়ে"],
        'expected_answer': "আত্মমর্যাদা"
    },
]

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

agent = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro',
    temperature=0.15
)
embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
qdrant = QdrantClient('"http://localhost:6333')
collection_name = 'hsc_helper'
total = len(evaluation_dataset)

def evaluate_relevance(evaluation_dataset):
    hits = 0

    for example in evaluation_dataset:
        context = retrieve(example['query'], embedding_model, qdrant, collection_name)
        if all(keyword in context for keyword in example['expected_context_keywords']):
            hits += 1

    print(f'Retrieval Relevance Accurace: {hits}/{total} = {hits/total:.2f}')

def evaluate_groundedness(evaluation_dataset):
    grounded_hits = 0

    for example in evaluation_dataset:
        context = retrieve(example['query'], embedding_model, qdrant, collection_name)
        prompt = generate_prompt_template(example['query'], context)
        response = agent.invoke(prompt).content.strip()

        if example['expected_answer'] in response:
            grounded_hits += 1

    print(f'Grounded Accuracy: {grounded_hits}/{total} = {grounded_hits/total:.2f}')

def evaluate_cosine_similarity(evaluation_dataset):
    print("Average Cosine Similarity Between Query and Chunks")

    for example in evaluation_dataset:
        context_chunks = retrieve(example['query'], embedding_model, qdrant, collection_name).split("\n\n")

        query_embedding = embedding_model.encode(example["query"], convert_to_tensor=True)

        chunk_embeddings = embedding_model.encode(context_chunks, convert_to_tensor=True)

        similarity = util.cos_sim(query_embedding, chunk_embeddings).mean().item()

        print(f"Query: {example['query'][:30]}... \nAverage Cosine Similarity: {similarity:.4f}\n")

if __name__ == "__main__":
    evaluate_relevance(evaluation_dataset)
    evaluate_groundedness(evaluation_dataset)
    evaluate_cosine_similarity(evaluation_dataset)

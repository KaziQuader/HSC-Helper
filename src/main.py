from prepare_data import create_vector_db
from rag import generate, get_transformed_query
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from collections import deque
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
agent = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro',
    temperature=0.15
)
memory = deque(maxlen=2)
chat_history = None

def main():
    qdrant, collection_name = create_vector_db('data/HSC26-Bangla1st-Paper.pdf', 'clean/full_text.txt', embedding_model)

    # user_request = input('Please Enter Your Query: ')
    user_requests = ['বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?']
    for user_request in user_requests:
        agent_response = generate(user_request, agent, embedding_model, chat_history, memory, qdrant, collection_name)
        print(agent_response)

if __name__ == "__main__":
    main()
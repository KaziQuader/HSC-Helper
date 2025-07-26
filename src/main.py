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

embedding_model = SentenceTransformer("intfloat/multilingual-e5-base")
agent = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro',
    temperature=0.15
)
memory = deque(maxlen=5)
chat_history = None

def main():
    qdrant, collection_name = create_vector_db('data/HSC26-Bangla1st-Paper.pdf', 'clean/full_text.txt', embedding_model)

    # user_request = input('Please Enter Your Query: ')
    user_requests = ['অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?', 'কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?', 'বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?', "Who has been referred to as Anupam's god of fortune?", 'According to Anupam, who is referred to as a noble/good man?', "What was Kalyani's actual age at the time of marriage?"]
    for user_request in user_requests:
        agent_response = generate(user_request, agent, embedding_model, chat_history, memory, qdrant, collection_name)
        print(agent_response)

if __name__ == "__main__":
    main()
import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from prompt_template import generate_prompt_template, transform_query_prompt
from collections import deque
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

qdrant = QdrantClient("http://localhost:6333")
collection_name = 'hsc_helper'
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
agent = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro',
    temperature=0.15
)
short_term_memory = deque(maxlen=2)
chat_history = None

def get_transformed_query(user_request, chat_history):
    response_schema = ResponseSchema(name="query", description="The standalone transformed query")
    parser = StructuredOutputParser.from_response_schemas([response_schema])
    print(chat_history)
    prompt = transform_query_prompt(user_request, chat_history)
    prompt += "\n\n" + parser.get_format_instructions()

    response = agent.invoke(prompt)
    parsed = parser.parse(response.content)

    query = parsed['query']
    return query

def retrieve(user_request):
    query_embedding = embedding_model.encode(user_request)
    results = qdrant.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        limit=5,
    )

    context_chunks = [point.payload["text"] for point in results.points]       
        
    # Join context texts into a single string
    context = "\n\n".join(context_chunks)
    return context

def generate(user_request):
    context = retrieve(user_request)
    prompt = generate_prompt_template(user_request, context)
    response = agent.invoke(prompt)
    print(response.content)

for i in range(5):
    user_request = input('Please Enter Your Query: ')
    transformed_request = get_transformed_query(user_request, chat_history)
    agent_response = generate(transformed_request)

    short_term_memory.append({'User':user_request, 'Assistant':agent_response})
    chat_history = '"""\n'
    for chat in short_term_memory:
        chat_history += f'User:{chat["User"]}\nAssistant:{chat["Assistant"]}\n'
    chat_history += '"""'

    print(chat_history)


# user_request = 'কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?'
# generate(user_request)

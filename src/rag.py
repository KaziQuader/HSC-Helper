from src.prompt_template import generate_prompt_template, transform_query_prompt
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

def get_transformed_query(user_request, chat_history, agent):
    response_schema = ResponseSchema(name="query", description="The standalone transformed query")
    parser = StructuredOutputParser.from_response_schemas([response_schema])
   
    prompt = transform_query_prompt(user_request, chat_history)
    prompt += "\n\n" + parser.get_format_instructions()

    response = agent.invoke(prompt)
    parsed = parser.parse(response.content)

    query = parsed['query']
    return query

def retrieve(user_request, embedding_model, qdrant, collection_name):
    query_embedding = embedding_model.encode(user_request, normalize_embeddings=True)
    results = qdrant.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        limit=10,
    )

    context_chunks = [point.payload["text"] for point in results.points]       
        
    # Join context texts into a single string
    context = "\n\n".join(context_chunks)
    return context

def create_chat_history(memory, user_request, agent_response, chat_history):
    memory.append({'User':user_request, 'Assistant':agent_response})

    chat_history = '"""\n'
    for chat in memory:
        chat_history += f'User:{chat["User"]}\nAssistant:{chat["Assistant"]}\n'
    chat_history += '"""'

    return chat_history

def generate(user_request, agent, embedding_model, chat_history, memory, qdrant, collection_name):
    # Transform the query if necessary
    print('Getting transformed query')
    transformed_request = get_transformed_query(user_request, chat_history, agent)

    # Retrieve Context Chunks from the VectorDB
    print('Retrieving Context')
    context = retrieve(transformed_request, embedding_model, qdrant, collection_name)

    # Generate the Prompt Template
    print('Generating Prompt Template')
    prompt = generate_prompt_template(transformed_request, context)

    # Invoke Agent to get response
    print('Generating Reponse')
    response = agent.invoke(prompt)

    # Create the Short Term Memory
    print('Creating Short Term Memory')
    chat_history = create_chat_history(memory, user_request, response.content, chat_history)

    return response.content, chat_history

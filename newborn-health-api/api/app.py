from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
import os
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from flask_cors import CORS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

# LangSmith
from langsmith import traceable

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'pr-sparkling-sustainment-79'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')


from pinecone import Pinecone

# Initialize Pinecone with API Key and Environment
API_KEY = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=API_KEY)

# Define the Pinecone index name
INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
index = pc.Index(INDEX_NAME)
print(index.describe_index_stats())


# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 relevant documents

retriever = RunnableLambda(
    lambda user_input: index.search_records(
        namespace=INDEX_NAME, 
        query={
            "inputs": {"text": user_input}, 
            "top_k": 3
        },
        # rerank={
        #     "model": "bge-reranker-v2-m3",
        #     "top_n": 3,
        #     "rank_fields": ["chunk_text"]
        # },
        fields=["id", "chunk_text", "file_name"]
    )
)

# result = retriever.invoke("Disease prevention")
# print(result)
# vectorstore = Chroma(persist_directory="chroma_store", embedding_function=OpenAIEmbeddings())
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 relevant documents

# Initialize LLM and prompt
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a medical assistant that provides concise and professional responses."),
    # MessagesPlaceholder(variable_name="history_messages"),
    ("system", "Use the following retrieved context to answer the user's question:\n{context}"),
    ("human", "{input_user_message}")
])

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]



retriever_chain = RunnableLambda(
    lambda inputs: retriever.invoke(inputs["input_user_message"])  # Pass only the query to the retriever
)
# context = retriever_chain | (lambda docs: "\n\n".join(f"{doc.fields} (Source: {doc.metadata.get('source', 'Unknown')})" for doc in docs) if docs else "No relevant context found.")
context = retriever | (lambda docs: "\n\n".join(doc['fields']['chunk_text'] for doc in docs['result']['hits']) if docs else "No relevant context found.")
# print("Context:")
# print(context.invoke("Disease prevention"))

first_step = RunnablePassthrough.assign(context=lambda x: retriever.invoke(x["input_user_message"]))

runnable = RunnableParallel(
    response=
    {"input_user_message": RunnablePassthrough(), 
     "context":(lambda docs: "\n\n".join(doc['fields']['chunk_text'] for doc in docs['context']['result']['hits']) if docs else "No relevant context found.")}
    | prompt | llm | StrOutputParser(),
    relevant_docs=lambda x: [
        {"id": doc['_id'], "metadata": doc['fields']['file_name']}
        for doc in x['context']['result']['hits']
        # for doc in x["context"]
    ]
)
rag_chain = first_step | runnable

# print(retriever.invoke("Common illness"))
# print(rag_chain.invoke({"input_user_message": "Common illness"}))

chain_with_message_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input_user_message",
    history_messages_key="history_messages",
)

# print(first_step.invoke({"input_user_message": "What is the capital of France?"}))
# print(rag_chain.invoke({"input_user_message": "What is the capital of France?"}))

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@traceable
@app.route('/ask', methods=['POST'])
def ask():
    name = request.form.get('name')

    

    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Debugging: Print the question
    print(f"Question: {question}")

    session_id = "1234"
    
    response = chain_with_message_history.invoke(
        {
            "input_user_message": question
        },
        config={"configurable": {"session_id": session_id}}
    )

    # response = chain_with_message_history.invoke(question, config={"configurable": {"session_id": "1"}})
    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name = name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

    # Debugging: Print the response
    print(f"Response: {response}")

    return jsonify(response)
    # return jsonify({"response": response})

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'development':
        app.run(debug=True)
    else:
        # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
        app.run(debug=False)

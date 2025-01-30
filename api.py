from flask import Flask, request, jsonify
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

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'pr-sparkling-sustainment-79'
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')

vectorstore = Chroma(persist_directory="chroma_store", embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 relevant documents

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
context = retriever_chain | (lambda docs: "\n\n".join(f"{doc.page_content} (Source: {doc.metadata.get('source', 'Unknown')})" for doc in docs) if docs else "No relevant context found.")

first_step = RunnablePassthrough.assign(context=lambda x: retriever.invoke(x["input_user_message"]))

runnable = RunnableParallel(
    response=
    {"input_user_message": RunnablePassthrough(), 
     "context":(lambda docs: "\n\n".join(f"{doc.page_content})" for doc in docs["context"]) if docs else "No relevant context found.")}
    | prompt | llm | StrOutputParser(),
    relevant_docs=lambda x: [
        {"id": doc.id, "metadata": doc.metadata}
        for doc in x["context"]
    ]
)
rag_chain = first_step | runnable


chain_with_message_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input_user_message",
    history_messages_key="history_messages",
)

# print(first_step.invoke({"input_user_message": "What is the capital of France?"}))
# print(rag_chain.invoke({"input_user_message": "What is the capital of France?"}))

@traceable
@app.route('/ask', methods=['POST'])
def ask():
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

    # Debugging: Print the response
    print(f"Response: {response}")

    return jsonify(response)
    # return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import os
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate  # Add this import
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv  # Add this import
from flask_cors import CORS  # Add this import

# LangSmith
import openai
from langsmith import wrappers, traceable

# Load environment variables from .env file
load_dotenv()  # Add this line

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'pr-sparkling-sustainment-79'
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')


vectorstore = Chroma(persist_directory="chroma_store", embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Initialize LLM and prompt
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
# prompt = hub.pull("rlm/rag-prompt")
prompt = ChatPromptTemplate.from_messages(
    messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['context', 'question'], input_types={}, partial_variables={}, 
template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:"""), additional_kwargs={})]
)

# Define the RAG chain
rag_chain = (
    # {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)), "question": RunnablePassthrough()}
    {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@traceable
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "Question is required"}), 400

    response = rag_chain.invoke(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
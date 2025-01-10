from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma  # Updated import path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
import openai

# Load environment variables from .env file
load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'pr-sparkling-sustainment-79'
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')

# Directory containing PDFs
pdf_directory = "./pdfs/"

# Initialize text splitter and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = OpenAIEmbeddings()

# Initialize Chroma vector store with persistent storage and embedding function
vectorstore = Chroma(persist_directory="./chroma_store", embedding_function=embeddings)

# Load and process all PDFs in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_directory, filename))
        docs = loader.load()
        splits = text_splitter.split_documents(docs)
        vectorstore.add_documents(documents=splits)


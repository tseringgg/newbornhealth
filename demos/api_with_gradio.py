import os
from flask import Flask
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from flask_cors import CORS
import gradio as gr  # Add this import
from langchain.chains import ConversationalRetrievalChain  # Add this import
from langchain.memory import ConversationBufferMemory  # Add this import
from langchain import hub  # Add this import

# LangSmith
import openai
from langsmith import wrappers, traceable

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
retriever = vectorstore.as_retriever()

# Initialize LLM and prompt
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
prompt = hub.pull("rlm/rag-prompt")

memory = ConversationBufferMemory()

conversation = ConversationalRetrievalChain(
    llm=llm,
    memory=memory
)

with gr.Blocks() as chat_system:
    chat = gr.Chatbot()
    prompt = gr.Textbox(placeholder="What's on your mind?")
    clear = gr.ClearButton([prompt, chat])
    clear.click(conversation.memory.clear)

    def llm_reply(prompt, chat_history):
        reply = conversation.predict(input=prompt)
        chat_history.append((prompt, reply))
        return "", chat_history

    prompt.submit(llm_reply, [prompt, chat], [prompt, chat])



if __name__ == "__main__":
    chat_system.launch()
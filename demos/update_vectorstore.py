import os
import pinecone
from pinecone import Pinecone
from PyPDF2 import PdfFileReader
# from openai.embeddings_utils import get_embedding
from openai import get_embedding
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone with API Key and Environment
API_KEY = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=API_KEY)

# Define the Pinecone index name
INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
index = pc.Index(INDEX_NAME)

# Load all PDF files from the "pdfs" folder
pdf_folder = 'pdfs'
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Loop through each PDF file:
for pdf_file in pdf_files:
    file_path = os.path.join(pdf_folder, pdf_file)
    with open(file_path, 'rb') as f:
        reader = PdfFileReader(f)
        text = ''
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()

    # Split the text into chunks for better vector storage
    text_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    # Generate embeddings for each text chunk using OpenAI Embeddings
    embeddings = [get_embedding(chunk) for chunk in text_chunks]

    # Create metadata containing the filename and relevant details
    metadata = [{'filename': pdf_file, 'chunk_index': i} for i in range(len(text_chunks))]

    # Store the embeddings and metadata in the Pinecone vectorstore
    for embedding, meta in zip(embeddings, metadata):
        index.upsert([(meta['filename'] + '_' + str(meta['chunk_index']), embedding, meta)])

# Print a confirmation message once all PDFs are processed
print("All PDFs have been processed and stored in the Pinecone vectorstore.")

# Exit the script

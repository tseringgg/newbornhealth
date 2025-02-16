import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from PyPDF2.errors import DependencyError
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
print(INDEX_NAME)
REGION = "us-west-2"  # Adjust based on your Pinecone account region

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

print("Existing indexes:")
print(pc.list_indexes())

# Check if the index already exists, create if needed
existing_indexes = pc.list_indexes()
if not any(index["name"] == INDEX_NAME for index in existing_indexes):
    print(f"Creating new index: {INDEX_NAME}")
    index_model = pc.create_index_for_model(
        name=INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "multilingual-e5-large",
            "field_map": {"text": "chunk_text", "text": "file_name"}
        }
    )

# Connect to the newly created index
index = pc.Index(INDEX_NAME)

# Function to extract and chunk text from a PDF
def extract_text_from_pdf(pdf_path, chunk_size=1000):
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Get list of PDFs from the /pdfs folder
pdf_folder = "../pdfs"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Prepare data for upserting
data_to_upsert = []
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    text_chunks = extract_text_from_pdf(pdf_path)

    for i, chunk in enumerate(text_chunks):
        data_to_upsert.append({
            "id": f"{pdf_file.replace('.pdf', '')}_{i}",  # Use filename and chunk index as ID
            "chunk_text": chunk,  # Store text chunk for inference
            "file_name": pdf_file  # Store filename for reference
        })

print(f"Extracted {len(data_to_upsert)} text chunks from {len(pdf_files)} PDFs.")

try:
    from Crypto.Cipher import AES
except ImportError:
    raise DependencyError("PyCryptodome is required for AES algorithm")

# Function to split data into smaller chunks
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Upsert data into Pinecone index in smaller chunks
CHUNK_SIZE = 10  # Adjust the chunk size as needed
if data_to_upsert:
    for chunk in chunk_data(data_to_upsert, CHUNK_SIZE):
        index.upsert_records(namespace=INDEX_NAME, records=chunk)
    print(f"Upserted {len(data_to_upsert)} PDF documents into {INDEX_NAME}.")
else:
    print("No valid PDFs found for upsert.")

print("Indexing complete!")

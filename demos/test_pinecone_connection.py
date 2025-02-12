import os
import pinecone
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone with API Key and Environment
API_KEY = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=API_KEY)

# Define the Pinecone index name
INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
index = pc.Index(INDEX_NAME)

# Upsert some test data
test_data = [
    ("test_id_1", [0.1, 0.2, 0.3], {"metadata_key": "metadata_value_1"}),
    ("test_id_2", [0.4, 0.5, 0.6], {"metadata_key": "metadata_value_2"})
]

index.upsert(test_data)

# Print a confirmation message
print("Test data has been upserted to the Pinecone index.")

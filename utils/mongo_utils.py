from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()  # make sure your .env is in the root folder

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

if not all([MONGO_URI, MONGO_DB, MONGO_COLLECTION]):
    raise ValueError("Please set MONGO_URI, MONGO_DB, and MONGO_COLLECTION in your .env file")

# -----------------------
# Connect to MongoDB
# -----------------------
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# -----------------------
# Function to insert a single document
# -----------------------
def save_document(doc: dict) -> str:
    """
    Inserts a JSON-like document into MongoDB.
    Adds a timestamp if not already present.
    Returns the inserted document ID as a string.
    """
    if not isinstance(doc, dict):
        raise ValueError("Document must be a dictionary")

    # Add creation timestamp if missing
    if "created_at" not in doc:
        doc["created_at"] = datetime.utcnow()

    result = collection.insert_one(doc)
    return str(result.inserted_id)


# -----------------------
# Function to insert multiple documents
# -----------------------
def save_documents(docs: list[dict]) -> list[str]:
    """
    Inserts multiple documents into MongoDB.
    Adds timestamps if missing.
    Returns a list of inserted IDs.
    """
    if not isinstance(docs, list):
        raise ValueError("Docs must be a list of dictionaries")
    
    for doc in docs:
        if not isinstance(doc, dict):
            raise ValueError("Each document must be a dictionary")
        if "created_at" not in doc:
            doc["created_at"] = datetime.utcnow()

    result = collection.insert_many(docs)
    return [str(_id) for _id in result.inserted_ids]


# -----------------------
# Optional: test connection
# -----------------------
def test_connection():
    try:
        client.admin.command("ping")
        print(f"✅ Connected to MongoDB database: {MONGO_DB}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

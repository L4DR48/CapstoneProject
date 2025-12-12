from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

if not all([MONGO_URI, MONGO_DB, MONGO_COLLECTION]):
    raise ValueError("Please set MONGO_URI, MONGO_DB, and MONGO_COLLECTION in your .env file")


# Connect to MongoDB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


# Function to insert a single document

def save_document(doc: dict) -> str:
    """
    Inserts a JSON-like document into MongoDB.
    Adds a timestamp if not already present.
    Returns the inserted document ID as a string.
    """
    if not isinstance(doc, dict):
        raise ValueError("Document must be a dictionary")
    if "created_at" not in doc:
        doc["created_at"] = datetime.utcnow()

    result = collection.insert_one(doc)
    return str(result.inserted_id)

def get_documents_from_mongo(filter_query: dict):
    """
    Returns a list of MongoDB documents matching the filter.
    Converts ObjectId values to strings so model can read them.
    """
    results = list(collection.find(filter_query))
    
    for doc in results:
        doc["_id"] = str(doc["_id"])
    
    return results



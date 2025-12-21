from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Singleton client
_client = None
_collection = None

def init_mongo():
    """
    Initialize MongoDB connection using environment variables.
    Returns the collection handle.
    Safe to call multiple times in Streamlit.
    """
    global _client, _collection

    load_dotenv()  # ensure env vars are loaded

    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

    if not all([MONGO_URI, MONGO_DB, MONGO_COLLECTION]):
        raise ValueError("Please set MONGO_URI, MONGO_DB, and MONGO_COLLECTION in your .env file")

    if _client is None:
        _client = MongoClient(MONGO_URI)

    if _collection is None:
        db = _client[MONGO_DB]
        _collection = db[MONGO_COLLECTION]

    return _collection






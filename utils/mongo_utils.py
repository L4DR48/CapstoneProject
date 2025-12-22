from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import pandas as pd
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
        _client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

    if _collection is None:
        db = _client[MONGO_DB]
        _collection = db[MONGO_COLLECTION]

    return _collection


def store_boxscore(boxscore: dict, team_name: str, opponent):
    """
    Store a boxscore in MongoDB using the init_mongo() collection.
    Returns the inserted document ID.
    """
    collection = init_mongo()

    doc = {
        "team_name": team_name,
        "opponent": opponent, 
        "timestamp": pd.Timestamp.now(),  # optional
        "boxscore": boxscore
    }

    result = collection.insert_one(doc)
    return result.inserted_id




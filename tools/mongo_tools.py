from datetime import datetime
from utils.mongo_utils import collection, db, client


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
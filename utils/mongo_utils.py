from pymongo import MongoClient
from dotenv import load_dotenv
import os


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






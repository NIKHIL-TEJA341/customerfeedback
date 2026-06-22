import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = None
db = None
reviews_col = None

if MONGO_URI and MONGO_URI != "your_mongodb_connection_string_here":
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client["feedbacknlp"]
        reviews_col = db["reviews"]
        reports_col = db["reports"]
        print("Connected to MongoDB Atlas successfully.")
    except Exception as e:
        print(f"MongoDB connection error: {e}")

def insert_review(review_data):
    if reviews_col is not None:
        reviews_col.insert_one(review_data)

def get_all_reviews():
    if reviews_col is not None:
        return list(reviews_col.find({}, {"_id": 0}))
    return []

def insert_bulk_reviews(reviews_list):
    if reviews_col is not None and reviews_list:
        reviews_col.insert_many(reviews_list)

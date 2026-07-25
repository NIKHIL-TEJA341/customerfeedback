import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    MONGO_URI = st.secrets["MONGO_URI"]
except Exception:
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
    """Fetches original records for Demo Mode (records without user_email)."""
    if reviews_col is not None:
        return list(reviews_col.find({"user_email": {"$exists": False}}, {"_id": 0}))
    return []

def insert_bulk_reviews(reviews_list):
    if reviews_col is not None and reviews_list:
        reviews_col.insert_many(reviews_list)

# --- User Scoped Functions ---

def get_user_reviews(user_email):
    """Fetches records specific to a logged-in user."""
    if reviews_col is not None:
        return list(reviews_col.find({"user_email": user_email}, {"_id": 0}))
    return []

def insert_review_for_user(user_email, review_data):
    """Inserts a single review for a logged-in user."""
    if reviews_col is not None:
        review_data["user_email"] = user_email
        reviews_col.insert_one(review_data)

def insert_bulk_reviews_for_user(user_email, reviews_list):
    """Inserts bulk reviews for a logged-in user."""
    if reviews_col is not None and reviews_list:
        for r in reviews_list:
            r["user_email"] = user_email
        reviews_col.insert_many(reviews_list)


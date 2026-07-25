import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.ui_utils import load_css
load_css()
import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.predictor import predict_sentiment
from src.database import insert_review_for_user
from src.auth import require_auth, get_current_user_email


st.title("🔍 Analyze Single Feedback")
st.markdown("<p class='hero-subtitle'>Input a customer review below to instantly predict its sentiment using our trained AI model.</p>", unsafe_allow_html=True)

require_auth()
user_email = get_current_user_email()
if not user_email:
    st.warning("👀 **Demo Mode**: You can test the AI sentiment prediction, but results will NOT be saved to the database.")

with st.form("analyze_form"):
    col1, col2 = st.columns(2)
    with col1:
        cust_id = st.text_input("Customer ID", placeholder="e.g. C001")
        cust_name = st.text_input("Customer Name", placeholder="e.g. John Doe")
        category = st.selectbox("Category", ["Electronics", "Apparel", "Home", "Books", "Other"])
    with col2:
        product = st.text_input("Product Name", placeholder="e.g. Smartphone X")
        rating = st.slider("Rating (Optional/Actual)", 1, 5, 4)
        date = st.date_input("Review Date", datetime.date.today())
        
    feedback = st.text_area("Feedback Text", placeholder="Type the customer's review here...", height=150)
    
    submitted = st.form_submit_button("Analyze Sentiment ✨", use_container_width=True)

if submitted:
    if not feedback.strip():
        st.error("Please enter some feedback text.")
    else:
        with st.spinner("Analyzing semantics..."):
            sentiment, confidence = predict_sentiment(feedback)
            
            st.markdown("### Analysis Result")
            st.markdown("---")
            rc1, rc2, rc3 = st.columns(3)
            
            color = "green" if sentiment == "Positive" else "red" if sentiment == "Negative" else "gray"
            emoji = "😊" if sentiment == "Positive" else "😡" if sentiment == "Negative" else "😐"
            
            with rc1:
                st.markdown(f"<h3 style='color: {color};'>Sentiment: {sentiment} {emoji}</h3>", unsafe_allow_html=True)
            with rc2:
                st.metric(label="AI Confidence Score", value=f"{confidence}%")
             
            doc = {
                "customer_id": cust_id,
                "customer_name": cust_name,
                "product": product,
                "category": category,
                "rating": rating,
                "feedback": feedback,
                "sentiment": sentiment,
                "confidence": confidence,
                "date": date.strftime("%Y-%m-%d")
            }
            if user_email:
                insert_review_for_user(user_email, doc)
                st.success("✅ Analysis complete! Result saved securely to your private workspace.")
            else:
                st.info("ℹ️ **Demo Mode**: Sentiment analyzed successfully, but result was NOT saved.")

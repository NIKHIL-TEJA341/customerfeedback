import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.ui_utils import load_css
load_css()
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.database import get_all_reviews

st.set_page_config(page_title="Feedback History", page_icon="📜", layout="wide")

st.title("📜 Feedback History")
st.markdown("<p class='hero-subtitle'>Search and filter previously analyzed reviews from the database.</p>", unsafe_allow_html=True)

reviews = get_all_reviews()

if not reviews:
    st.info("No reviews found in the database.")
else:
    df = pd.DataFrame(reviews)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sentiment_filter = st.multiselect("Filter by Sentiment", options=["Positive", "Neutral", "Negative"], default=["Positive", "Neutral", "Negative"])
    
    with col2:
        if 'category' in df.columns:
            categories = df['category'].unique().tolist()
            cat_filter = st.multiselect("Filter by Category", options=categories, default=categories)
        else:
            cat_filter = []
            
    with col3:
        search_term = st.text_input("Search Product or Feedback")
        
    filtered_df = df[df['sentiment'].isin(sentiment_filter)]
    if cat_filter and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(cat_filter)]
        
    if search_term:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]
        
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} total reviews**")
    st.dataframe(filtered_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export View to CSV",
        data=csv,
        file_name='feedback_history.csv',
        mime='text/csv',
    )

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
from src.ai_insights import generate_insights

st.set_page_config(page_title="AI Insights Center", page_icon="🧠", layout="wide")

st.title("🧠 AI Insights Center")
st.markdown("<p class='hero-subtitle'>Premium Feature: Using advanced LLMs to automatically read and summarize massive volumes of customer feedback into actionable business intelligence.</p>", unsafe_allow_html=True)

reviews = get_all_reviews()

if not reviews:
    st.info("No reviews found in the database. Add some reviews to generate insights.")
else:
    df = pd.DataFrame(reviews)
    
    st.markdown("---")
    st.markdown(f"**Ready to analyze {len(df)} reviews in the database.**")
    
    if st.button("Generate Executive Insights ✨", use_container_width=True):
        with st.spinner("Connecting to Groq API to analyze all textual feedback..."):
            texts = df['feedback'].dropna().tolist()
            if not texts:
                st.error("No valid feedback text found.")
            else:
                insights_markdown = generate_insights(texts)
                
                if "Groq API Key not configured" in insights_markdown:
                    st.error(insights_markdown)
                else:
                    st.success("Analysis Complete!")
                    st.markdown("### 📊 Executive Summary Report")
                    with st.container(border=True):
                        st.markdown(insights_markdown)

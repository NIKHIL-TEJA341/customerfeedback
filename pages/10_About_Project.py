import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.ui_utils import load_css
load_css()

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Sentix AI")

st.markdown("""
### 🎯 Project Overview
Sentix AI is an industry-oriented Customer Feedback Sentiment Analysis & Business Intelligence Dashboard.
It automates the process of reading and classifying thousands of customer reviews into Positive, Neutral, or Negative sentiment.

### ⚙️ Technology Stack
- **Frontend**: Streamlit
- **Backend & ML**: Python, Scikit-Learn (Random Forest & TF-IDF), NLTK, XGBoost
- **Database**: MongoDB Atlas
- **Generative AI**: Groq API (LLaMA-3)
- **Visualizations**: Plotly, Matplotlib, WordCloud

### 🧠 Machine Learning Pipeline
1. **Data Ingestion**: Raw Amazon Consumer Reviews CSVs.
2. **Preprocessing**: Lowercasing, punctuation removal, and NLTK stopword filtering.
3. **Vectorization**: TF-IDF Vectorizer extracting up to 10,000 features.
4. **Classification**: Trained using Random Forest Classifier optimized with `class_weight='balanced'` to handle imbalanced datasets.
5. **Deployment**: Saved as serialized `.pkl` files and loaded natively into this dashboard.

### 🏢 Key Features
- **Real-Time Analysis**: Single review prediction.
- **Bulk CSV Analysis**: Upload and predict hundreds of reviews instantly.
- **Trend Monitoring**: Track brand health over time.
- **AI Insights**: LLM-powered root-cause identification and executive summaries.

---
**Developed by Nikhil Teja.**
""")

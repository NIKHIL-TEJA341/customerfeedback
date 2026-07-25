import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
import datetime
from src.predictor import predict_sentiment
from src.database import insert_bulk_reviews_for_user
from src.auth import require_auth, get_current_user_email


st.title("📁 Bulk CSV Analysis")
st.markdown("<p class='hero-subtitle'>Upload a CSV file containing hundreds or thousands of reviews to analyze them all at once.</p>", unsafe_allow_html=True)

require_auth()
user_email = get_current_user_email()
if not user_email:
    st.warning("👀 **Demo Mode**: You can analyze CSV files, but results will NOT be saved to the database.")

uploaded_file = st.file_uploader("Upload Reviews CSV", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.dataframe(df.head())
         
        text_cols = [c for c in df.columns if 'text' in c.lower() or 'review' in c.lower() or 'feedback' in c.lower()]
        
        if not text_cols:
            st.error("Could not automatically find a text/feedback column. Please ensure your CSV has a column named 'feedback' or 'review'.")
        else:
            selected_col = st.selectbox("Select the column containing the feedback text:", text_cols)
            
            if st.button("Start Bulk Analysis 🚀", use_container_width=True):
                with st.spinner("Analyzing bulk data... Please wait..."):
                    
                    results = []
                    db_docs = []
                       
                    progress_bar = st.progress(0)
                    total_rows = len(df)
                    
                    for idx, row in df.iterrows():
                        text = str(row[selected_col])
                        sentiment, conf = predict_sentiment(text)
                        
                        results.append({
                            "Feedback": text,
                            "Sentiment": sentiment,
                            "Confidence (%)": conf
                        })
                        
                        db_docs.append({
                            "customer_id": f"BULK_{idx}",
                            "customer_name": "Bulk Upload",
                            "product": str(row.get('product', 'Unknown')),
                            "category": str(row.get('category', 'Bulk')),
                            "rating": row.get('rating', 0),
                            "feedback": text,
                            "sentiment": sentiment,
                            "confidence": conf,
                            "date": datetime.date.today().strftime("%Y-%m-%d")
                        })
                                      
                        if idx % max(1, (total_rows // 20)) == 0:
                            progress_bar.progress(min(1.0, idx / total_rows))
                    
                    progress_bar.progress(1.0)          
                    if user_email:
                        insert_bulk_reviews_for_user(user_email, db_docs)
                        st.success(f"✅ Successfully analyzed {total_rows} reviews and saved to your workspace!")
                    else:
                        st.info(f"ℹ️ **Demo Mode**: {total_rows} reviews analyzed successfully, but NOT saved.")
                    
                                  
                    res_df = pd.DataFrame(results)
                    st.dataframe(res_df)
                                     
                    csv_export = res_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Results CSV",
                        data=csv_export,
                        file_name='analyzed_reviews.csv',
                        mime='text/csv',
                    )
    except Exception as e:
        st.error(f"Error reading file: {e}")

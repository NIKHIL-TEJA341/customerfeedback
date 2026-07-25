import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.ui_utils import load_css
load_css()
import pandas as pd
from fpdf import FPDF
import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.database import get_all_reviews, get_user_reviews
from src.auth import require_auth, get_current_user_email


st.title("📄 Reports Center")
st.markdown("<p class='hero-subtitle'>Generate and download comprehensive Business Intelligence reports.</p>", unsafe_allow_html=True)

require_auth()
user_email = get_current_user_email()

if user_email:
    reviews = get_user_reviews(user_email)
else:
    reviews = get_all_reviews()
    st.warning("👀 **Demo Mode**: Viewing sample data. Changes will not be saved.")

if not reviews:
    st.info("No reviews found in the database.")
else:
    df = pd.DataFrame(reviews)
    
    st.markdown("### Export Data")
    
    st.markdown("#### Download Raw Data (CSV)")
    csv_export = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Dataset CSV",
        data=csv_export,
        file_name=f'sentix_export_{datetime.date.today()}.csv',
        mime='text/csv',
    )
    
    st.markdown("---")
    
    st.markdown("#### Generate Executive PDF Report")
    
    if st.button("Generate PDF Report", use_container_width=True):
        with st.spinner("Compiling PDF Report..."):
            total = len(df)
            pos = len(df[df['sentiment'] == 'Positive'])
            neg = len(df[df['sentiment'] == 'Negative'])
            neu = len(df[df['sentiment'] == 'Neutral'])
            
            pos_rate = (pos / total) * 100 if total > 0 else 0
            neg_rate = (neg / total) * 100 if total > 0 else 0
            
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Sentix AI - Executive Sentiment Report", ln=1, align='C')
    
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(200, 10, f"Generated on: {datetime.date.today()}", ln=1, align='C')
            pdf.ln(10)
            

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, "Summary Metrics", ln=1)
            pdf.set_font("Arial", '', 11)
            pdf.cell(200, 10, f"Total Reviews Analyzed: {total}", ln=1)
            pdf.cell(200, 10, f"Positive Reviews: {pos} ({pos_rate:.1f}%)", ln=1)
            pdf.cell(200, 10, f"Negative Reviews: {neg} ({neg_rate:.1f}%)", ln=1)
            pdf.cell(200, 10, f"Neutral Reviews: {neu}", ln=1)
            pdf.ln(10)
            
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, "Product Highlights", ln=1)
            pdf.set_font("Arial", '', 11)
            
            if 'product' in df.columns:
                prod_stats = df.groupby('product')['sentiment'].value_counts().unstack(fill_value=0)
                prod_stats['Total'] = prod_stats.sum(axis=1)
                for col in ['Positive', 'Negative', 'Neutral']:
                    if col not in prod_stats.columns:
                        prod_stats[col] = 0
                prod_stats['Positive Rate'] = (prod_stats['Positive'] / prod_stats['Total']) * 100
                
                meaningful = prod_stats[prod_stats['Total'] >= 2]
                if meaningful.empty:
                    meaningful = prod_stats
                    
                top_prods = meaningful.sort_values(by='Positive Rate', ascending=False).head(3)
                
                pdf.cell(200, 10, "Top Performing Products:", ln=1)
                for prod in top_prods.index:
                    
                    safe_prod = str(prod).encode('ascii', 'ignore').decode('ascii')
                    pdf.cell(200, 10, f"- {safe_prod}", ln=1)
            
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(200, 10, "Powered by Sentix AI Machine Learning Pipeline.", ln=1, align='C')
            
            pdf_output_path = os.path.join(os.path.dirname(__file__), "Sentix_Report.pdf")
            pdf.output(pdf_output_path)
            
            with open(pdf_output_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                
            st.success("PDF Generated Successfully!")
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"Sentix_Report_{datetime.date.today()}.pdf",
                mime="application/pdf"
            )

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.ui_utils import load_css
load_css()
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.database import get_all_reviews

st.set_page_config(page_title="Product Analytics", page_icon="🛍️", layout="wide")

st.title("🛍️ Product Analytics")
st.markdown("<p class='hero-subtitle'>Discover which products are driving customer loyalty and which need immediate attention.</p>", unsafe_allow_html=True)

reviews = get_all_reviews()

if not reviews:
    st.info("No reviews found in the database.")
else:
    df = pd.DataFrame(reviews)
    
    if 'product' not in df.columns or df['product'].nunique() == 0:
        st.warning("No product data available in the reviews.")
    else:
        st.markdown("### Top Performing Products (Most Loved)")
          
        prod_stats = df.groupby('product')['sentiment'].value_counts().unstack(fill_value=0)
        prod_stats['Total'] = prod_stats.sum(axis=1)
        
        for col in ['Positive', 'Negative', 'Neutral']:
            if col not in prod_stats.columns:
                prod_stats[col] = 0
                
        prod_stats['Positive Rate'] = (prod_stats['Positive'] / prod_stats['Total']) * 100
        prod_stats['Negative Rate'] = (prod_stats['Negative'] / prod_stats['Total']) * 100
          
        meaningful_prods = prod_stats[prod_stats['Total'] >= 2]
        if meaningful_prods.empty:
            meaningful_prods = prod_stats 
            
        top_loved = meaningful_prods.sort_values(by='Positive Rate', ascending=False).head(10)
        
        fig_loved = px.bar(
            top_loved.reset_index(), 
            y='product', 
            x='Positive Rate', 
            orientation='h',
            title='Top Products by Positive Sentiment (%)',
            color_discrete_sequence=['#22c55e']
        )
        fig_loved.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_loved, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### Products Needing Attention (Most Complained)")
        
        top_complained = meaningful_prods.sort_values(by='Negative Rate', ascending=False).head(10)
        top_complained = top_complained[top_complained['Negative Rate'] > 0]
        
        if not top_complained.empty:
            fig_complained = px.bar(
                top_complained.reset_index(), 
                y='product', 
                x='Negative Rate', 
                orientation='h',
                title='Bottom Products by Negative Sentiment (%)',
                color_discrete_sequence=['#ef4444']
            )
            fig_complained.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_complained, use_container_width=True)
        else:
            st.success("No products have negative reviews yet!")

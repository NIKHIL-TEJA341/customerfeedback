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

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Enterprise Dashboard")
st.markdown("<p class='hero-subtitle'>Real-time sentiment aggregation and key performance indicators.</p>", unsafe_allow_html=True)

reviews = get_all_reviews()

if not reviews:
    st.info("No reviews found in the database. Go to 'Analyze Feedback' or 'Bulk Analysis' to add some!")
else:
    df = pd.DataFrame(reviews)
     
    total = len(df)
    pos = len(df[df['sentiment'] == 'Positive'])
    neg = len(df[df['sentiment'] == 'Negative'])
    neu = len(df[df['sentiment'] == 'Neutral'])
    
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Reviews Analyzed", total)
    with col2:
        st.metric("Positive Reviews", pos)
    with col3:
        st.metric("Negative Reviews", neg)
    with col4:
        st.metric("Neutral Reviews", neu)
        
    st.markdown("---")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### Sentiment Distribution")
        fig_pie = px.pie(
            names=['Positive', 'Negative', 'Neutral'],
            values=[pos, neg, neu],
            color=['Positive', 'Negative', 'Neutral'],
            color_discrete_map={'Positive':'#22c55e', 'Negative':'#ef4444', 'Neutral':'#94a3b8'},
            hole=0.4
        )
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with chart_col2:
        st.markdown("### Sentiment Over Time")
        if 'date' in df.columns:
            
            try:
                df['date'] = pd.to_datetime(df['date'])
                trend_df = df.groupby([pd.Grouper(key='date', freq='D'), 'sentiment']).size().reset_index(name='count')
                
                fig_line = px.line(
                    trend_df, 
                    x='date', 
                    y='count', 
                    color='sentiment',
                    color_discrete_map={'Positive':'#22c55e', 'Negative':'#ef4444', 'Neutral':'#94a3b8'},
                    markers=True
                )
                fig_line.update_layout(margin=dict(t=0, b=0, l=0, r=0), xaxis_title="Date", yaxis_title="Review Count")
                st.plotly_chart(fig_line, use_container_width=True)
            except Exception as e:
                st.warning("Could not parse date column for trend analysis.")
        else:
            st.warning("No date column found for trend analysis.")

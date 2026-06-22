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

st.set_page_config(page_title="Trend Monitoring", page_icon="📈", layout="wide")

st.title("📈 Trend Monitoring")
st.markdown("<p class='hero-subtitle'>Analyze longitudinal sentiment shifts and spot seasonal patterns.</p>", unsafe_allow_html=True)

reviews = get_all_reviews()

if not reviews:
    st.info("No reviews found in the database.")
else:
    df = pd.DataFrame(reviews)
    if 'date' not in df.columns:
        st.warning("No date column available for trend monitoring.")
    else:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        time_res = st.selectbox("Select Time Resolution", ["Daily", "Weekly", "Monthly"])
        
        if time_res == "Daily":
            freq = 'D'
        elif time_res == "Weekly":
            freq = 'W'
        else:
            freq = 'M'
            
        trend_df = df.groupby([pd.Grouper(key='date', freq=freq), 'sentiment']).size().reset_index(name='count')
        
        fig = px.area(
            trend_df,
            x='date',
            y='count',
            color='sentiment',
            title=f"{time_res} Sentiment Trends",
            color_discrete_map={'Positive':'#22c55e', 'Negative':'#ef4444', 'Neutral':'#94a3b8'},
        )
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Growth Indicators")
        recent = df.sort_values('date').tail(50)
        recent_pos = len(recent[recent['sentiment'] == 'Positive'])
        recent_rate = (recent_pos / len(recent)) * 100 if len(recent) > 0 else 0
        
        st.metric("Recent Positive Satisfaction Rate (Last 50 reviews)", f"{recent_rate:.1f}%")

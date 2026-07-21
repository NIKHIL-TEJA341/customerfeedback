import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Sentix AI | Customer Sentiment",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.ui_utils import load_css
load_css()

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

hero_img_path = os.path.join(os.path.dirname(__file__), "appimg.png")
hero_img_b64 = get_base64_of_bin_file(hero_img_path)
img_html = f'<img src="data:image/png;base64,{hero_img_b64}" style="width: 100%; max-width: 400px; border-radius: 12px; filter: drop-shadow(0 0 20px rgba(168, 85, 247, 0.4));">' if hero_img_b64 else ''

st.markdown(f"""
<style>
.hover-card {{
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.hover-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.6) !important;
}}
.hover-btn {{
    transition: transform 0.2s ease, filter 0.2s ease;
}}
.hover-btn:hover {{
    transform: scale(1.05);
    filter: brightness(1.2);
}}
</style>
<div class="hover-card" style="background-color: #0B1120; border: 1px solid #1E293B; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);">
    <div style="flex: 1; padding-right: 2rem;">
        <h1 style="font-size: 2.8rem; color: #F8FAFC; margin-bottom: 0.5rem; font-weight: 800; line-height: 1.1;">AI-Powered<br><span style="background: linear-gradient(90deg, #A855F7, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Sentiment Analysis</span></h1>
        <h3 style="color: #818CF8; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">Transform Customer Feedback into Actionable Insights</h3>
        <p style="color: #94A3B8; font-size: 1rem; line-height: 1.6; margin-bottom: 2rem;">
            Decipher the emotional pulse of your global customer base. Sentix AI uses advanced linguistics to process millions of reviews, turning subjective noise into objective strategy.
        </p>
        <div style="display: flex; gap: 1rem;">
            <a href="/Analyze_Feedback" target="_self" class="hover-btn" style="background: linear-gradient(90deg, #6366F1, #A855F7); color: white; padding: 0.8rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);">Analyze Feedback &rarr;</a>
            <a href="/Dashboard" target="_self" class="hover-btn" style="background-color: transparent; border: 1px solid #334155; color: #F8FAFC; padding: 0.8rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">View Dashboard 
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#F8FAFC" width="18" height="18"><path d="M3 3h8v8H3V3zm0 10h8v8H3v-8zm10-10h8v8h-8V3zm0 10h8v8h-8v-8z"/></svg>
            </a>
        </div>
    </div>
    <div style="flex: 0 0 320px; display: flex; justify-content: flex-end;">
        {img_html}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.custom-metric-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 2rem;
}
.custom-metric-card {
    background-color: #0B1120;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 1.25rem;
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.custom-metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
}
.metric-icon-box {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

from src.database import get_all_reviews
import pandas as pd

reviews = get_all_reviews()
total_reviews = len(reviews)
pos_rate = 0
neg_rate = 0
active_products = 0

if total_reviews > 0:
    df = pd.DataFrame(reviews)
    if 'sentiment' in df.columns:
        pos_count = len(df[df['sentiment'] == 'Positive'])
        neg_count = len(df[df['sentiment'] == 'Negative'])
        pos_rate = round((pos_count / total_reviews) * 100)
        neg_rate = round((neg_count / total_reviews) * 100)
    
    if 'product' in df.columns:
        active_products = df['product'].replace('', pd.NA).dropna().nunique()

st.markdown(f"""
<div class="custom-metric-container">
    <div class="custom-metric-card">
        <div class="metric-icon-box" style="background-color: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.2);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#A855F7" width="32" height="32"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-6 9h-4v2h4v-2zm4-4H6v2h12V7zm0 8h-8v2h8v-2z"/></svg>
        </div>
        <div>
            <div style="color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px;">Reviews Processed</div>
            <div style="color: #F8FAFC; font-size: 1.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px;">{total_reviews}</div>
            <div style="display: inline-block; background-color: rgba(16, 185, 129, 0.1); color: #10B981; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">&uarr; Live</div>
        </div>
    </div>
    <div class="custom-metric-card">
        <div class="metric-icon-box" style="background-color: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#10B981" width="32" height="32"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/></svg>
        </div>
        <div>
            <div style="color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px;">Positive Rate</div>
            <div style="color: #F8FAFC; font-size: 1.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px;">{pos_rate}%</div>
        </div>
    </div>
    <div class="custom-metric-card">
        <div class="metric-icon-box" style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#EF4444" width="32" height="32"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 3c-2.33 0-4.31 1.46-5.11 3.5h10.22c-.8-2.04-2.78-3.5-5.11-3.5z"/></svg>
        </div>
        <div>
            <div style="color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px;">Negative Rate</div>
            <div style="color: #F8FAFC; font-size: 1.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px;">{neg_rate}%</div>
        </div>
    </div>
    <div class="custom-metric-card">
        <div class="metric-icon-box" style="background-color: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.2);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0EA5E9" width="32" height="32"><path d="M21 16.5c0 .38-.21.71-.53.88l-7.9 4.44c-.16.12-.36.18-.57.18-.21 0-.41-.06-.57-.18l-7.9-4.44A.991.991 0 013 16.5v-9c0-.38.21-.71.53-.88l7.9-4.44c.16-.12.36-.18.57-.18.21 0 .41.06.57.18l7.9 4.44c.32.17.53.5.53.88v9zM12 4.15L6.04 7.5 12 10.85l5.96-3.35L12 4.15zM5 15.91l6 3.38v-6.71L5 9.21v6.7zm14 0v-6.7l-6 3.38v6.71l6-3.38z"/></svg>
        </div>
        <div>
            <div style="color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px;">Active Products</div>
            <div style="color: #F8FAFC; font-size: 1.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px;">{active_products}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="background-color: #0B1120; border: 1px solid #1E293B; border-radius: 16px; padding: 2rem;">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#A855F7" width="24" height="24" style="margin-right: 10px;"><path d="M12 2L14.26 8.74L21 11L14.26 13.26L12 20L9.74 13.26L3 11L9.74 8.74L12 2Z"/></svg>
<h2 style="color: #F8FAFC; font-size: 1.8rem; font-weight: 800; margin: 0;">Core Capabilities</h2>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#64748B" width="20" height="20" style="margin-left: 10px;"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>
</div>
<p style="color: #94A3B8; font-size: 1rem; margin-bottom: 2rem;">High-Precision Intelligence: Sentix AI bridges the gap between raw textual data and strategic decision-making using proprietary NLP models.</p>

<div style="display: flex; gap: 1rem;">
<div class="hover-card" style="flex: 1; background-color: #050810; border: 1px solid #1E293B; border-radius: 12px; padding: 1.25rem; position: relative;">
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
<div style="background-color: rgba(168, 85, 247, 0.1); padding: 8px; border-radius: 8px;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#A855F7" width="20" height="20"><path d="M7 2v11h3v9l7-12h-4l4-8z"/></svg>
</div>
<div style="color: #A855F7; font-weight: 700; font-size: 1.1rem;">Real-Time Analysis</div>
</div>
<p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;">Instant feedback processing and continuous insights.</p>
<div style="position: absolute; bottom: 1.25rem; right: 1.25rem; background-color: #1E293B; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#94A3B8" width="16" height="16"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
</div>
</div>

<div class="hover-card" style="flex: 1; background-color: #050810; border: 1px solid #1E293B; border-radius: 12px; padding: 1.25rem; position: relative;">
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
<div style="background-color: rgba(16, 185, 129, 0.1); padding: 8px; border-radius: 8px;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#10B981" width="20" height="20"><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.25 2.52.75-1.23-3.5-2.07V8h-1.5z"/></svg>
</div>
<div style="color: #10B981; font-weight: 700; font-size: 1.1rem;">AI Insights</div>
</div>
<p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;">Automated root-cause identification and sentiment understanding.</p>
<div style="position: absolute; bottom: 1.25rem; right: 1.25rem; background-color: #1E293B; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#94A3B8" width="16" height="16"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
</div>
</div>

<div class="hover-card" style="flex: 1; background-color: #050810; border: 1px solid #1E293B; border-radius: 12px; padding: 1.25rem; position: relative;">
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
<div style="background-color: rgba(245, 158, 11, 0.1); padding: 8px; border-radius: 8px;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#F59E0B" width="20" height="20"><path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/></svg>
</div>
<div style="color: #F59E0B; font-weight: 700; font-size: 1.1rem;">Trend Monitoring</div>
</div>
<p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;">Longitudinal data tracking. Spot emerging patterns before they impact growth.</p>
<div style="position: absolute; bottom: 1.25rem; right: 1.25rem; background-color: #1E293B; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#94A3B8" width="16" height="16"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
</div>
</div>

<div class="hover-card" style="flex: 1; background-color: #050810; border: 1px solid #1E293B; border-radius: 12px; padding: 1.25rem; position: relative;">
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
<div style="background-color: rgba(236, 72, 153, 0.1); padding: 8px; border-radius: 8px;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#EC4899" width="20" height="20"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
</div>
<div style="color: #EC4899; font-weight: 700; font-size: 1.1rem;">Business Reports</div>
</div>
<p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;">Board-ready PDF and interactive executive dashboards.</p>
<div style="position: absolute; bottom: 1.25rem; right: 1.25rem; background-color: #1E293B; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#94A3B8" width="16" height="16"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

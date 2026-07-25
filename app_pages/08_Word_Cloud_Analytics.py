import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from src.database import get_all_reviews, get_user_reviews
from src.auth import require_auth, get_current_user_email


st.title("☁️ Word Cloud Analytics")
st.markdown("<p class='hero-subtitle'>Visual representation of the most frequently used keywords in Positive and Negative feedback.</p>", unsafe_allow_html=True)

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
    
    pos_reviews = " ".join(df[df['sentiment'] == 'Positive']['feedback'].dropna().astype(str).tolist())
    neg_reviews = " ".join(df[df['sentiment'] == 'Negative']['feedback'].dropna().astype(str).tolist())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Positive Keywords")
        if pos_reviews.strip():
            wordcloud_pos = WordCloud(width=800, height=400, background_color='#F8F9FA', colormap='Greens').generate(pos_reviews)
            fig_pos, ax_pos = plt.subplots(figsize=(10, 5))
            ax_pos.imshow(wordcloud_pos, interpolation='bilinear')
            ax_pos.axis("off")
            st.pyplot(fig_pos)
        else:
            st.info("No positive words to display.")
            
    with col2:
        st.markdown("### Negative Keywords")
        if neg_reviews.strip():
            wordcloud_neg = WordCloud(width=800, height=400, background_color='#F8F9FA', colormap='Reds').generate(neg_reviews)
            fig_neg, ax_neg = plt.subplots(figsize=(10, 5))
            ax_neg.imshow(wordcloud_neg, interpolation='bilinear')
            ax_neg.axis("off")
            st.pyplot(fig_neg)
        else:
            st.info("No negative words to display.")

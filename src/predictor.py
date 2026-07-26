import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure the VADER lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

def predict_sentiment(text):
    """
    Predicts sentiment using VADER instead of the pre-trained ML model.
    Returns the predicted class ("Positive", "Negative", "Neutral") and a confidence score.
    """
    if not text or not str(text).strip():
        return "Neutral", 0.0
        
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    # Typical VADER thresholds
    if compound >= 0.05:
        sentiment_str = "Positive"
        confidence = compound
    elif compound <= -0.05:
        sentiment_str = "Negative"
        confidence = abs(compound)
    else:
        sentiment_str = "Neutral"
        # For neutral, use the 'neu' score as the confidence metric
        confidence = scores['neu']
        
    return sentiment_str, round(confidence * 100, 2)

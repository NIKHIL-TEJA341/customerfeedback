import os
import pickle

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
META_PATH = os.path.join(MODEL_DIR, "model_meta.txt")
VEC_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

try:
    with open(META_PATH, 'r') as f:
        model_filename = f.read().strip()
    # Check if a .gz version exists
    if os.path.exists(os.path.join(MODEL_DIR, model_filename + ".gz")):
        MODEL_PATH = os.path.join(MODEL_DIR, model_filename + ".gz")
    else:
        MODEL_PATH = os.path.join(MODEL_DIR, model_filename)
except FileNotFoundError:
    if os.path.exists(os.path.join(MODEL_DIR, "best_model_random_forest.pkl.gz")):
        MODEL_PATH = os.path.join(MODEL_DIR, "best_model_random_forest.pkl.gz")
    else:
        MODEL_PATH = os.path.join(MODEL_DIR, "best_model_random_forest.pkl")

model = None
vectorizer = None

try:
    import gzip
    if MODEL_PATH.endswith('.gz'):
        with gzip.open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    else:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
            
    with open(VEC_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print(f"Warning: Could not load model or vectorizer. Did you put them in the models/ folder? Error: {e}")

sentiment_map = {0: "Negative", 1: "Neutral", 2: "Positive"}

def predict_sentiment(text):
    if not model or not vectorizer:
        return "Error", 0.0
    
    vec_text = vectorizer.transform([text])
    try:
        probs = model.predict_proba(vec_text)[0]
        pred_class = probs.argmax()
        confidence = probs[pred_class]
    except:
        pred_class = model.predict(vec_text)[0]
        confidence = 1.0
        
    sentiment_str = sentiment_map.get(int(pred_class), "Neutral")
    return sentiment_str, round(confidence * 100, 2)

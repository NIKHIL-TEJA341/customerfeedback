import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    client = Groq(api_key=GROQ_API_KEY)
except:
    client = None

def generate_insights(reviews_text_list):
    if not client or GROQ_API_KEY == "your_groq_api_key_here":
        return "Groq API Key not configured. Please add it to your .env file."
        
    combined_text = "\n".join(reviews_text_list[:100])
    
    prompt = f"""
    You are an expert AI business analyst for 'Sentix AI'. 
    Analyze the following customer reviews and extract:
    1. Top 3 Complaints (with a brief example)
    2. Top 3 Praises (with a brief example)
    3. 3 Key Business Recommendations to improve customer satisfaction.
    
    Format the response using clean Markdown.
    
    Reviews:
    {combined_text}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a highly analytical, professional business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {e}"

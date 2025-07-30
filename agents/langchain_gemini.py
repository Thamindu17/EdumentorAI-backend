from langchain_google_genai import ChatGoogleGenerativeAI
from agents.config import GOOGLE_API_KEY

def get_gemini_model():
    return ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",  
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7
    )

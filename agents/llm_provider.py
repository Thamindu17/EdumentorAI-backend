from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from agents.config import (
    LLM_PROVIDER, 
    GROQ_API_KEY, 
    HUGGINGFACE_API_TOKEN,
    GROQ_MODEL,
    HUGGINGFACE_MODEL
)

def get_llm_model():
    """
    Returns the appropriate LLM model based on the configured provider.
    Supports Groq and Hugging Face.
    """
    if LLM_PROVIDER.lower() == "groq":
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required when using Groq provider")
        
        return ChatGroq(
            model=GROQ_MODEL,
            groq_api_key=GROQ_API_KEY,
            temperature=0.7,
            max_tokens=1024
        )
    
    elif LLM_PROVIDER.lower() == "huggingface":
        if not HUGGINGFACE_API_TOKEN:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN is required when using Hugging Face provider")
        
        # Create HuggingFace endpoint
        llm_endpoint = HuggingFaceEndpoint(
            repo_id=HUGGINGFACE_MODEL,
            huggingfacehub_api_token=HUGGINGFACE_API_TOKEN,
            temperature=0.7
        )
        
        # Wrap it in ChatHuggingFace for chat functionality
        return ChatHuggingFace(llm=llm_endpoint)
    
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}. Supported providers: 'groq', 'huggingface'")

# Backward compatibility alias
def get_gemini_model():
    """Deprecated: Use get_llm_model() instead"""
    return get_llm_model()

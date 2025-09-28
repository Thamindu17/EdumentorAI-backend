import os
from dotenv import load_dotenv

load_dotenv()

# LLM Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # Options: "groq", "huggingface"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Model configurations
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

import google.generativeai as genai
from agents.config import GOOGLE_API_KEY  # Or paste your key directly here

genai.configure(api_key="AIzaSyAaRzB8OuAtOQ-wyc8_iIX2W2QhgLkRjj4")

try:
    models = genai.list_models()

    print("\n✅ Available Models with Supported Generation Methods:\n")
    for model in models:
        print(f"🧠 {model.name} | Supports generation: {'generateContent' in model.supported_generation_methods}")
except Exception as e:
    print(f"\n❌ Error: {e}")

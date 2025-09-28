from agents.llm_provider import get_llm_model
from agents.config import LLM_PROVIDER

try:
    print(f"\n✅ Testing {LLM_PROVIDER.upper()} LLM Connection:\n")
    
    # Test the LLM model
    llm = get_llm_model()
    test_response = llm.invoke("Say hello and confirm the LLM is working properly.")
    
    print(f"✅ {LLM_PROVIDER.upper()} connection successful!")
    print(f"Test response: {test_response.content}")
    
    print(f"\nCurrent LLM Provider: {LLM_PROVIDER}")
    print("You can change the provider by setting LLM_PROVIDER in your .env file to 'groq' or 'huggingface'")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Make sure you have set the appropriate API key in your .env file:")
    if LLM_PROVIDER.lower() == "groq":
        print("- GROQ_API_KEY=your_groq_api_key")
    elif LLM_PROVIDER.lower() == "huggingface":
        print("- HUGGINGFACEHUB_API_TOKEN=your_huggingface_token")

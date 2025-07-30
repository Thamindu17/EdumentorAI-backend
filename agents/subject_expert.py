from agents.langchain_gemini import get_gemini_model
from langchain_core.prompts import PromptTemplate

def explain_concept(concept):
    llm = get_gemini_model()
    prompt = PromptTemplate(
        input_variables=["concept"],
        template="You are a subject expert. Explain the concept '{concept}' simply and clearly."
    )
    chain = prompt | llm
    result = chain.invoke({"concept": concept})
    return result.content

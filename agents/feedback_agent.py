from langchain_core.prompts import PromptTemplate
from agents.langchain_gemini import get_gemini_model

def generate_feedback(student_answer: str, expected_answer: str) -> str:
    llm = get_gemini_model()

    prompt = PromptTemplate(
        input_variables=["student_answer", "expected_answer"],
        template=(
            "You are a teacher providing constructive feedback. Compare the student's answer: '{student_answer}' "
            "to the expected answer: '{expected_answer}'. Point out strengths, weaknesses, and how to improve."
        ),
    )

    chain = prompt | llm
    result = chain.invoke({
        "student_answer": student_answer,
        "expected_answer": expected_answer
    })

    return result.content

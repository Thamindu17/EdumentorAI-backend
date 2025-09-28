from langchain_core.prompts import PromptTemplate
from agents.llm_provider import get_llm_model

def generate_feedback(student_answer: str, expected_answer: str) -> str:
    llm = get_llm_model()

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

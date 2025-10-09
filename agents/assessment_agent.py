from langchain_core.prompts import PromptTemplate
from agents.llm_provider import get_llm_model

def assess_answer(student_answer: str, sample_answer: str) -> str:
    """Assess student answer against a sample answer"""
    llm = get_llm_model()
    
    prompt = PromptTemplate(
        input_variables=["student_answer", "sample_answer"],
        template=(
            "You are an educational assessment expert. Compare the student's answer: '{student_answer}' "
            "to the sample answer: '{sample_answer}'. "
            "Provide a detailed assessment including:\n"
            "1. Accuracy score (1-10)\n"
            "2. Key concepts covered\n"
            "3. Missing elements\n"
            "4. Overall feedback\n"
            "5. Suggestions for improvement"
        )
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "student_answer": student_answer,
        "sample_answer": sample_answer
    })
    
    return result.content

def generate_exam_questions(topic: str, question_type: str = "mixed", num_questions: int = 5) -> str:
    llm = get_llm_model()

    prompt = PromptTemplate(
        input_variables=["topic", "question_type", "num_questions"],
        template=(
            "You are an experienced teacher creating exam questions. Generate {num_questions} {question_type} "
            "questions for the topic '{topic}'. Make sure questions are relevant and appropriately challenging for high school level."
        )
    )

    

    chain = prompt | llm
    result = chain.invoke({
        "topic": topic,
        "question_type": question_type,
        "num_questions": num_questions
    })

    return result.content

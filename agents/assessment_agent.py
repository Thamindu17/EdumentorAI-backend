from langchain_core.prompts import PromptTemplate
from agents.llm_provider import get_llm_model

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

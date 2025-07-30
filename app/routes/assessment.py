from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.assessment_agent import generate_exam_questions

router = APIRouter()

class QuestionInput(BaseModel):
    topic: str
    question_type: str = "mixed"  # e.g., MCQ, short answer, essay
    num_questions: int = 5

@router.post("/")
def get_exam_questions(data: QuestionInput):
    try:
        questions = generate_exam_questions(
            topic=data.topic,
            question_type=data.question_type,
            num_questions=data.num_questions
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

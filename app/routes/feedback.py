from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.feedback_agent import generate_feedback

router = APIRouter()

class FeedbackInput(BaseModel):
    student_answer: str
    expected_answer: str

@router.post("/")
def get_feedback(data: FeedbackInput):
    try:
        result = generate_feedback(data.student_answer, data.expected_answer)
        return {"feedback": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

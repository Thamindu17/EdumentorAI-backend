from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.curriculum_planner import get_curriculum_plan

router = APIRouter()

class CurriculumInput(BaseModel):
    subject: str
    hours_per_day: float
    exam_date: str  # ISO format: "2025-09-15"

@router.post("/")
def plan_curriculum(data: CurriculumInput):
    try:
        result = get_curriculum_plan(
            subject=data.subject,
            hours_per_day=data.hours_per_day,
            exam_date=data.exam_date
        )
        return {"curriculum_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# agents/curriculum_planner.py
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from agents.langchain_gemini import get_gemini_model

def get_curriculum_plan(subject, hours_per_day, exam_date):
    llm = get_gemini_model()

    today = datetime.now().date()
    exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
    days_remaining = (exam - today).days

    if days_remaining <= 0:
        return "⚠️ The exam date has already passed or is today. Please select a valid future date."

    prompt = PromptTemplate(
        input_variables=["subject", "hours", "exam_date", "days_remaining"],
        template=(
            "You are an expert curriculum planner. Create a detailed study plan for the subject '{subject}'. "
            "The student can study {hours} hours per day and has {days_remaining} days left until the exam on {exam_date}. "
            "Please create a compact, day-by-day or week-by-week curriculum with achievable goals."
        ),
    )

    chain = prompt | llm
    result = chain.invoke({
        "subject": subject,
        "hours": hours_per_day,
        "exam_date": exam_date,
        "days_remaining": days_remaining
    })

    return result.content
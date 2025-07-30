from fastapi import FastAPI
from app.routes import curriculum,feedback,assessment
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title="EduMentorAI",
    description="Multi-agent backend powered by LangChain and Gemini",
    version="0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add route
app.include_router(curriculum.router, prefix="/api/curriculum", tags=["Curriculum Planner"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback Generator"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["Exam Question Generator"])
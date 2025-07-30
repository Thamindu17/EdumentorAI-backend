# test_curriculum.py
from agents.curriculum_planner import get_curriculum_plan

subject = "Machine Learning"
hours = 2
exam_date = "2025-09-15"

plan = get_curriculum_plan(subject, hours, exam_date)
print(plan)

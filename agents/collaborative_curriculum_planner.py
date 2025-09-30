"""
Enhanced Curriculum Planner with Collaboration Capabilities
Creates personalized study plans while collaborating with other agents
"""

from typing import Dict, Any
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from agents.base_agent import BaseAgent


class CollaborativeCurriculumPlanner(BaseAgent):
    """Enhanced curriculum planner that collaborates with other agents"""
    
    def __init__(self):
        super().__init__("curriculum_planner", "Educational Curriculum Planning Expert")
    
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing with collaboration support"""
        subject = inputs.get("subject")
        hours_per_day = inputs.get("hours_per_day")
        exam_date = inputs.get("exam_date")
        
        # Get collaboration context from other agents
        assessment_context = self.get_context("assessment_results")
        explanation_context = self.get_context("concept_explanation")
        
        curriculum_plan = self.get_curriculum_plan_collaborative(
            subject, 
            hours_per_day, 
            exam_date,
            assessment_context,
            explanation_context
        )
        
        # Store result for other agents
        self.set_context("curriculum_plan", curriculum_plan)
        self.log_step("curriculum_planning", curriculum_plan)
        
        # Request difficulty analysis from assessment agent if available
        if assessment_context:
            self._request_difficulty_analysis()
        
        return {
            "curriculum_plan": curriculum_plan,
            "collaboration_context": self.get_collaboration_context()
        }
    
    def get_curriculum_plan_collaborative(self, subject: str, hours_per_day: float, exam_date: str,
                                        assessment_context: Any = None, explanation_context: Any = None) -> str:
        """Create curriculum plan with collaboration context"""
        
        today = datetime.now().date()
        exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
        days_remaining = (exam - today).days

        if days_remaining <= 0:
            return "⚠️ The exam date has already passed or is today. Please select a valid future date."

        collaboration_data = {
            "previous_insights": assessment_context if assessment_context else "No assessment data available",
            "shared_analysis": explanation_context if explanation_context else "No concept explanation available",
            "agent_feedback": self._get_recent_feedback()
        }
        
        base_template = (
            "You are an expert curriculum planner. Create a detailed study plan for the subject '{subject}'. "
            "The student can study {hours} hours per day and has {days_remaining} days left until the exam on {exam_date}. "
            "Please create a compact, day-by-day or week-by-week curriculum with achievable goals."
        )
        
        prompt = self.create_collaborative_prompt(base_template, collaboration_data)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "subject": subject,
            "hours": hours_per_day,
            "exam_date": exam_date,
            "days_remaining": days_remaining,
            "previous_insights": collaboration_data["previous_insights"],
            "shared_analysis": collaboration_data["shared_analysis"],
            "agent_feedback": collaboration_data["agent_feedback"]
        })

        return result.content
    
    def process_message(self, message):
        """Process messages from other agents"""
        if message.message_type == "collaboration_request":
            task = message.content.get("task")
            if task == "adjust_curriculum":
                return self._adjust_curriculum_based_on_assessment(message.content)
            elif task == "create_remedial_plan":
                return self._create_remedial_plan(message.content)
        elif message.message_type == "difficulty_analysis":
            self._incorporate_difficulty_analysis(message.content)
    
    def _request_difficulty_analysis(self):
        """Request difficulty analysis from assessment agent"""
        assessment_results = self.get_context("assessment_results")
        
        analysis_request = {
            "task": "difficulty_analysis",
            "assessment_results": assessment_results,
            "requestor": self.agent_id
        }
        
        self.send_message("assessment_agent", analysis_request, "collaboration_request")
    
    def _adjust_curriculum_based_on_assessment(self, request_data: Dict[str, Any]) -> str:
        """Adjust curriculum based on assessment results"""
        weak_areas = request_data.get("weak_areas", [])
        strong_areas = request_data.get("strong_areas", [])
        original_plan = self.get_context("curriculum_plan")
        
        prompt = PromptTemplate(
            input_variables=["original_plan", "weak_areas", "strong_areas"],
            template=(
                "Adjust this study plan: '{original_plan}' based on assessment results. "
                "Allocate more time to weak areas: {weak_areas} "
                "and optimize time for strong areas: {strong_areas}. "
                "Provide a revised, balanced curriculum."
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "original_plan": original_plan,
            "weak_areas": ", ".join(weak_areas),
            "strong_areas": ", ".join(strong_areas)
        })
        
        # Update stored curriculum plan
        self.set_context("curriculum_plan", result.content)
        
        return result.content
    
    def _create_remedial_plan(self, request_data: Dict[str, Any]) -> str:
        """Create additional remedial study plan for difficult topics"""
        concept = request_data.get("concept")
        weak_points = request_data.get("weak_points", [])
        available_time = request_data.get("available_time", "2 hours")
        
        prompt = PromptTemplate(
            input_variables=["concept", "weak_points", "available_time"],
            template=(
                "Create a focused remedial study plan for '{concept}'. "
                "Address these specific weak points: {weak_points}. "
                "Plan should fit within {available_time} and include:\n"
                "1. Review materials needed\n"
                "2. Practice exercises\n"
                "3. Self-assessment checkpoints\n"
                "4. Timeline breakdown"
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "concept": concept,
            "weak_points": ", ".join(weak_points),
            "available_time": available_time
        })
        
        return result.content
    
    def _incorporate_difficulty_analysis(self, analysis_data: Dict[str, Any]):
        """Incorporate difficulty analysis into curriculum planning"""
        difficulty_analysis = analysis_data.get("difficulty_analysis")
        
        # Store analysis for future curriculum adjustments
        self.set_context("difficulty_analysis", difficulty_analysis)
        
        # Send feedback to assessment agent about curriculum implications
        feedback_data = {
            "message": "Difficulty analysis incorporated into curriculum planning",
            "curriculum_adjustments": "Time allocation adjusted based on difficulty levels",
            "from_agent": self.agent_id
        }
        
        self.send_message("assessment_agent", feedback_data, "feedback")
    
    def _get_recent_feedback(self) -> str:
        """Get recent feedback from other agents"""
        feedback_messages = [msg for msg in self.inbox if msg.message_type == "feedback"]
        if feedback_messages:
            return f"Recent feedback: {feedback_messages[-1].content}"
        return "No recent feedback available"


# Backward compatibility function
def get_curriculum_plan(subject: str, hours_per_day: float, exam_date: str) -> str:
    """Backward compatibility wrapper"""
    planner = CollaborativeCurriculumPlanner()
    result = planner.process({
        "subject": subject,
        "hours_per_day": hours_per_day,
        "exam_date": exam_date
    })
    return result["curriculum_plan"]
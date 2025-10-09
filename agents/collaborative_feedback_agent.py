"""
Enhanced Feedback Agent with Collaboration Capabilities
Provides comprehensive feedback while collaborating with other agents
"""

from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from agents.base_agent import BaseAgent


class CollaborativeFeedbackAgent(BaseAgent):
    """Enhanced feedback agent that collaborates with other agents"""
    
    def __init__(self):
        super().__init__("feedback_agent", "Educational Feedback Expert")
    
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing with collaboration support"""
        student_answer = inputs.get("student_answer")
        expected_answer = inputs.get("expected_answer")
        
        # Get collaboration context from other agents
        assessment_context = self.get_context("assessment_results")
        explanation_context = self.get_context("concept_explanation")
        curriculum_context = self.get_context("curriculum_plan")
        
        feedback = self.generate_feedback_collaborative(
            student_answer,
            expected_answer,
            assessment_context,
            explanation_context,
            curriculum_context
        )
        
        # Store result and provide feedback to other agents
        self.set_context("feedback_results", feedback)
        self.log_step("feedback_generation", feedback)
        
        # Send improvement suggestions to curriculum planner
        self._send_curriculum_suggestions(feedback)
        
        return {
            "feedback": feedback,
            "collaboration_context": self.get_collaboration_context()
        }
    
    def generate_feedback_collaborative(self, student_answer: str, expected_answer: str,
                                      assessment_context: Any = None, explanation_context: Any = None,
                                      curriculum_context: Any = None) -> str:
        """Generate feedback with full collaboration context"""
        
        collaboration_data = {
            "previous_insights": assessment_context if assessment_context else "No assessment context available",
            "shared_analysis": explanation_context if explanation_context else "No explanation context available",
            "agent_feedback": curriculum_context if curriculum_context else "No curriculum context available"
        }
        
        base_template = (
            "You are a teacher providing comprehensive constructive feedback. "
            "Compare the student's answer: '{student_answer}' "
            "to the expected answer: '{expected_answer}'. "
            "Provide detailed feedback including:\n"
            "1. What the student did well (strengths)\n"
            "2. Areas that need improvement (specific gaps)\n"
            "3. Misconceptions to address\n"
            "4. Specific study recommendations\n"
            "5. Encouragement and next steps\n"
            "6. Resources for improvement"
        )
        
        prompt = self.create_collaborative_prompt(base_template, collaboration_data)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "student_answer": student_answer,
            "expected_answer": expected_answer,
            "previous_insights": collaboration_data["previous_insights"],
            "shared_analysis": collaboration_data["shared_analysis"],
            "agent_feedback": collaboration_data["agent_feedback"]
        })
        
        return result.content
    
    def process_message(self, message):
        """Process messages from other agents"""
        if message.message_type == "collaboration_request":
            task = message.content.get("task")
            if task == "improvement_suggestions":
                return self._provide_improvement_suggestions(message.content)
            elif task == "motivational_feedback":
                return self._provide_motivational_feedback(message.content)
        elif message.message_type == "assessment_update":
            self._process_assessment_update(message.content)
    
    def _send_curriculum_suggestions(self, feedback: str):
        """Send curriculum improvement suggestions based on feedback"""
        weak_areas = self._extract_improvement_areas(feedback)
        
        if weak_areas:
            curriculum_suggestions = {
                "task": "adjust_curriculum",
                "weak_areas": weak_areas,
                "feedback_context": feedback,
                "suggestion_type": "improvement_focus"
            }
            
            self.send_message("curriculum_planner", curriculum_suggestions, "collaboration_request")
    
    def _extract_improvement_areas(self, feedback: str) -> list:
        """Extract specific areas needing improvement from feedback"""
        improvement_keywords = [
            "needs improvement", "should focus on", "work on", "strengthen",
            "missing", "unclear", "incorrect", "misconception"
        ]
        
        areas = []
        lines = feedback.split('\n')
        
        for line in lines:
            for keyword in improvement_keywords:
                if keyword in line.lower():
                    # Extract the concept/area mentioned in this line
                    area = line.strip()
                    if len(area) > 10:  # Ensure it's a meaningful line
                        areas.append(area)
                    break
        
        return areas[:5]  # Return top 5 improvement areas
    
    def _provide_improvement_suggestions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide specific improvement suggestions for other agents"""
        student_performance = request_data.get("student_performance")
        subject_area = request_data.get("subject_area")
        
        prompt = PromptTemplate(
            input_variables=["performance", "subject"],
            template=(
                "Based on this student performance: {performance} "
                "in {subject}, provide specific improvement strategies including:\n"
                "1. Study techniques\n"
                "2. Practice recommendations\n"
                "3. Timeline for improvement\n"
                "4. Success metrics"
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "performance": str(student_performance),
            "subject": subject_area
        })
        
        return {
            "improvement_suggestions": result.content,
            "provided_by": self.agent_id
        }
    
    def _provide_motivational_feedback(self, request_data: Dict[str, Any]) -> str:
        """Provide motivational feedback for struggling students"""
        student_struggles = request_data.get("struggles", [])
        achievements = request_data.get("achievements", [])
        
        prompt = PromptTemplate(
            input_variables=["struggles", "achievements"],
            template=(
                "Create encouraging, motivational feedback for a student. "
                "Their struggles: {struggles}. "
                "Their achievements: {achievements}. "
                "Focus on growth mindset, progress recognition, and confidence building."
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "struggles": ", ".join(student_struggles),
            "achievements": ", ".join(achievements)
        })
        
        return result.content
    
    def _process_assessment_update(self, update_data: Dict[str, Any]):
        """Process updates from assessment agent"""
        assessment_changes = update_data.get("changes")
        
        # Update feedback strategy based on new assessment information
        self.set_context("latest_assessment_update", assessment_changes)
        
        # Send acknowledgment back to assessment agent
        ack_data = {
            "message": "Assessment update processed and incorporated into feedback strategy",
            "from_agent": self.agent_id,
            "timestamp": update_data.get("timestamp")
        }
        
        self.send_message("assessment_agent", ack_data, "feedback")


# Backward compatibility function
def generate_feedback(student_answer: str, expected_answer: str) -> str:
    """Backward compatibility wrapper"""
    agent = CollaborativeFeedbackAgent()
    result = agent.process({
        "student_answer": student_answer,
        "expected_answer": expected_answer
    })
    return result["feedback"]
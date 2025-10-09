"""
Enhanced Subject Expert Agent with Collaboration Capabilities
Provides detailed explanations and collaborates with other agents
"""

from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from agents.base_agent import BaseAgent


class CollaborativeSubjectExpert(BaseAgent):
    """Enhanced subject expert that can collaborate with other agents"""
    
    def __init__(self):
        super().__init__("subject_expert", "Educational Content Expert")
    
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing with collaboration support"""
        concept = inputs.get("concept")
        student_level = inputs.get("student_level", "high school")
        
        # Check if assessment agent has provided context about student weaknesses
        assessment_context = self.get_context("assessment_results")
        curriculum_context = self.get_context("curriculum_plan")
        
        explanation = self.explain_concept_collaborative(
            concept, 
            student_level, 
            assessment_context, 
            curriculum_context
        )
        
        # Store result for other agents to use
        self.set_context("concept_explanation", explanation)
        self.log_step("concept_explanation", explanation)
        
        return {
            "explanation": explanation,
            "concept": concept,
            "collaboration_context": self.get_collaboration_context()
        }
    
    def explain_concept_collaborative(self, concept: str, student_level: str = "high school", 
                                   assessment_context: Any = None, curriculum_context: Any = None) -> str:
        """Explain concept with collaboration context"""
        
        # Build collaboration data
        collaboration_data = {
            "previous_insights": assessment_context if assessment_context else "No prior assessment available",
            "shared_analysis": curriculum_context if curriculum_context else "No curriculum context available",
            "agent_feedback": self._get_recent_agent_feedback()
        }
        
        base_template = (
            "You are a subject expert educator. Explain the concept '{concept}' "
            "clearly and simply for {student_level} level students. "
            "Make your explanation engaging and easy to understand."
        )
        
        prompt = self.create_collaborative_prompt(base_template, collaboration_data)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "concept": concept,
            "student_level": student_level,
            "previous_insights": collaboration_data["previous_insights"],
            "shared_analysis": collaboration_data["shared_analysis"],
            "agent_feedback": collaboration_data["agent_feedback"]
        })
        
        return result.content
    
    def process_message(self, message):
        """Process messages from other agents"""
        if message.message_type == "collaboration_request":
            task = message.content.get("task")
            if task == "clarify_concept":
                return self._clarify_concept_for_agent(message.content)
            elif task == "simplify_explanation":
                return self._simplify_explanation(message.content)
        elif message.message_type == "feedback":
            self._process_feedback(message.content)
    
    def _clarify_concept_for_agent(self, request_data: Dict[str, Any]) -> str:
        """Provide clarification for other agents"""
        concept = request_data.get("concept")
        specific_aspect = request_data.get("aspect")
        
        prompt = PromptTemplate(
            input_variables=["concept", "aspect"],
            template=(
                "Provide a focused clarification on the '{aspect}' aspect of '{concept}'. "
                "This is for another AI agent, so be precise and technical."
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"concept": concept, "aspect": specific_aspect})
        
        return result.content
    
    def _simplify_explanation(self, request_data: Dict[str, Any]) -> str:
        """Simplify explanation based on assessment results"""
        original_explanation = request_data.get("explanation")
        difficulty_areas = request_data.get("difficulty_areas", [])
        
        prompt = PromptTemplate(
            input_variables=["explanation", "difficulties"],
            template=(
                "Simplify this explanation: '{explanation}' "
                "Focus on clarifying these difficult areas: {difficulties}. "
                "Make it even more accessible for struggling students."
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "explanation": original_explanation,
            "difficulties": ", ".join(difficulty_areas)
        })
        
        return result.content
    
    def _get_recent_agent_feedback(self) -> str:
        """Get recent feedback from other agents"""
        feedback_messages = [msg for msg in self.inbox if msg.message_type == "feedback"]
        if feedback_messages:
            recent_feedback = feedback_messages[-1].content
            return f"Recent agent feedback: {recent_feedback}"
        return "No recent feedback from other agents"
    
    def _process_feedback(self, feedback_content: Dict[str, Any]):
        """Process feedback from other agents"""
        # Store feedback for future reference
        self.set_context("subject_expert_feedback", feedback_content)


# Backward compatibility function
def explain_concept(concept: str) -> str:
    """Backward compatibility wrapper"""
    expert = CollaborativeSubjectExpert()
    result = expert.process({"concept": concept})
    return result["explanation"]
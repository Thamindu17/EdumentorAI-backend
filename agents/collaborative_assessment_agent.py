"""
Enhanced Assessment Agent with Collaboration Capabilities
Generates questions and assessments while collaborating with other agents
"""

from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from agents.base_agent import BaseAgent


class CollaborativeAssessmentAgent(BaseAgent):
    """Enhanced assessment agent that collaborates with other agents"""
    
    def __init__(self):
        super().__init__("assessment_agent", "Educational Assessment Expert")
    
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing with collaboration support"""
        task_type = inputs.get("task_type", "assess_answer")
        
        if task_type == "assess_answer":
            return self._process_assessment(inputs)
        elif task_type == "generate_questions":
            return self._process_question_generation(inputs)
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    def _process_assessment(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process answer assessment with collaboration"""
        student_answer = inputs.get("student_answer")
        sample_answer = inputs.get("sample_answer")
        concept = inputs.get("concept")
        
        # Get collaboration context
        explanation_context = self.get_context("concept_explanation")
        curriculum_context = self.get_context("curriculum_plan")
        
        assessment_result = self.assess_answer_collaborative(
            student_answer, 
            sample_answer, 
            concept,
            explanation_context,
            curriculum_context
        )
        
        # Store results for other agents
        self.set_context("assessment_results", assessment_result)
        self.log_step("answer_assessment", assessment_result)
        
        # Send feedback to subject expert if student struggled
        if "needs improvement" in assessment_result.lower():
            self._request_clarification_from_expert(concept, assessment_result)
        
        return {
            "assessment": assessment_result,
            "collaboration_context": self.get_collaboration_context()
        }
    
    def _process_question_generation(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process question generation with collaboration"""
        topic = inputs.get("topic")
        question_type = inputs.get("question_type", "mixed")
        num_questions = inputs.get("num_questions", 5)
        
        # Get context from other agents
        explanation_context = self.get_context("concept_explanation")
        curriculum_context = self.get_context("curriculum_plan")
        
        questions = self.generate_exam_questions_collaborative(
            topic, 
            question_type, 
            num_questions,
            explanation_context,
            curriculum_context
        )
        
        self.set_context("generated_questions", questions)
        self.log_step("question_generation", questions)
        
        return {
            "questions": questions,
            "collaboration_context": self.get_collaboration_context()
        }
    
    def assess_answer_collaborative(self, student_answer: str, sample_answer: str, 
                                  concept: str = None, explanation_context: Any = None,
                                  curriculum_context: Any = None) -> str:
        """Assess answer with collaboration context"""
        
        collaboration_data = {
            "previous_insights": explanation_context if explanation_context else "No concept explanation available",
            "shared_analysis": curriculum_context if curriculum_context else "No curriculum context available",
            "agent_feedback": self._get_recent_feedback()
        }
        
        base_template = (
            "You are an educational assessment expert. Compare the student's answer: '{student_answer}' "
            "to the sample answer: '{sample_answer}'. "
            "Provide a detailed assessment including:\n"
            "1. Accuracy score (1-10)\n"
            "2. Key concepts covered\n"
            "3. Missing elements\n"
            "4. Overall feedback\n"
            "5. Specific areas needing improvement\n"
            "6. Recommendations for next steps"
        )
        
        prompt = self.create_collaborative_prompt(base_template, collaboration_data)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "student_answer": student_answer,
            "sample_answer": sample_answer,
            "previous_insights": collaboration_data["previous_insights"],
            "shared_analysis": collaboration_data["shared_analysis"],
            "agent_feedback": collaboration_data["agent_feedback"]
        })
        
        return result.content
    
    def generate_exam_questions_collaborative(self, topic: str, question_type: str = "mixed", 
                                            num_questions: int = 5, explanation_context: Any = None,
                                            curriculum_context: Any = None) -> str:
        """Generate questions with collaboration context"""
        
        collaboration_data = {
            "previous_insights": explanation_context if explanation_context else "No concept explanation available",
            "shared_analysis": curriculum_context if curriculum_context else "No curriculum context available",
            "agent_feedback": self._get_recent_feedback()
        }
        
        base_template = (
            "You are an experienced teacher creating exam questions. Generate {num_questions} {question_type} "
            "questions for the topic '{topic}'. Make sure questions are relevant and appropriately challenging for high school level."
        )
        
        prompt = self.create_collaborative_prompt(base_template, collaboration_data)
        
        chain = prompt | self.llm
        result = chain.invoke({
            "topic": topic,
            "question_type": question_type,
            "num_questions": num_questions,
            "previous_insights": collaboration_data["previous_insights"],
            "shared_analysis": collaboration_data["shared_analysis"],
            "agent_feedback": collaboration_data["agent_feedback"]
        })
        
        return result.content
    
    def process_message(self, message):
        """Process messages from other agents"""
        if message.message_type == "collaboration_request":
            task = message.content.get("task")
            if task == "difficulty_analysis":
                return self._analyze_difficulty(message.content)
            elif task == "create_targeted_questions":
                return self._create_targeted_questions(message.content)
        elif message.message_type == "clarification_request":
            self._process_clarification_request(message.content)
    
    def _request_clarification_from_expert(self, concept: str, assessment_result: str):
        """Request clarification from subject expert when student struggles"""
        difficult_areas = self._extract_difficulty_areas(assessment_result)
        
        clarification_request = {
            "task": "simplify_explanation",
            "explanation": self.get_context("concept_explanation"),
            "difficulty_areas": difficult_areas,
            "assessment_context": assessment_result
        }
        
        self.send_message("subject_expert", clarification_request, "collaboration_request")
    
    def _extract_difficulty_areas(self, assessment_result: str) -> List[str]:
        """Extract areas where student had difficulty"""
        # Simple keyword extraction - could be enhanced with NLP
        difficulty_keywords = ["missing", "incorrect", "unclear", "confused", "needs improvement"]
        areas = []
        
        for keyword in difficulty_keywords:
            if keyword in assessment_result.lower():
                # Extract context around the keyword
                lines = assessment_result.split('\n')
                for line in lines:
                    if keyword in line.lower():
                        areas.append(line.strip())
        
        return areas[:3]  # Return top 3 difficulty areas
    
    def _analyze_difficulty(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze difficulty level for curriculum planning"""
        assessment_results = request_data.get("assessment_results")
        
        prompt = PromptTemplate(
            input_variables=["assessment_results"],
            template=(
                "Analyze these assessment results and determine difficulty levels: {assessment_results}. "
                "Provide:\n"
                "1. Overall difficulty rating (1-10)\n"
                "2. Specific challenging concepts\n"
                "3. Recommended study time allocation\n"
                "4. Prerequisites that may be missing"
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"assessment_results": str(assessment_results)})
        
        return {
            "difficulty_analysis": result.content,
            "analyzed_by": self.agent_id
        }
    
    def _create_targeted_questions(self, request_data: Dict[str, Any]) -> str:
        """Create questions targeting specific weak areas"""
        weak_areas = request_data.get("weak_areas", [])
        topic = request_data.get("topic")
        
        prompt = PromptTemplate(
            input_variables=["topic", "weak_areas"],
            template=(
                "Create 3-5 targeted practice questions for '{topic}' "
                "focusing specifically on these weak areas: {weak_areas}. "
                "Questions should help students improve in these specific areas."
            )
        )
        
        chain = prompt | self.llm
        result = chain.invoke({
            "topic": topic,
            "weak_areas": ", ".join(weak_areas)
        })
        
        return result.content
    
    def _get_recent_feedback(self) -> str:
        """Get recent feedback from other agents"""
        feedback_messages = [msg for msg in self.inbox if msg.message_type == "feedback"]
        if feedback_messages:
            return f"Recent feedback: {feedback_messages[-1].content}"
        return "No recent feedback available"


# Backward compatibility functions
def assess_answer(student_answer: str, sample_answer: str) -> str:
    """Backward compatibility wrapper"""
    agent = CollaborativeAssessmentAgent()
    result = agent.process({
        "task_type": "assess_answer",
        "student_answer": student_answer,
        "sample_answer": sample_answer
    })
    return result["assessment"]

def generate_exam_questions(topic: str, question_type: str = "mixed", num_questions: int = 5) -> str:
    """Backward compatibility wrapper"""
    agent = CollaborativeAssessmentAgent()
    result = agent.process({
        "task_type": "generate_questions",
        "topic": topic,
        "question_type": question_type,
        "num_questions": num_questions
    })
    return result["questions"]
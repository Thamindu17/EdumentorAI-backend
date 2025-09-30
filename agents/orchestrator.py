from agents import assessment_agent, subject_expert
from agents.collaborative_orchestrator import CollaborativeOrchestrator

def run_workflow(student_answer, sample_answer, concept):
    """
    Enhanced workflow that supports both simple and collaborative modes
    """
    # Use collaborative orchestrator for enhanced functionality
    orchestrator = CollaborativeOrchestrator()
    
    # Run comprehensive collaborative workflow
    result = orchestrator.run_comprehensive_workflow(
        student_answer=student_answer,
        sample_answer=sample_answer,
        concept=concept,
        create_curriculum=False  # Don't create curriculum in basic workflow
    )
    
    return {
        "explanation": result.get("explanation"),
        "assessment": result.get("assessment"),
        "feedback": result.get("feedback"),
        "collaboration_summary": result.get("collaboration_summary"),
        "agent_interactions": result.get("agent_interactions")
    }

def run_simple_workflow(student_answer, sample_answer, concept):
    """
    Simple workflow using original agents (for backward compatibility)
    """
    explanation = subject_expert.explain_concept(concept)
    assessment = assessment_agent.assess_answer(student_answer, sample_answer)

    return {
        "explanation": explanation,
        "assessment": assessment
    }

def run_collaborative_workflow(student_answer, sample_answer, concept, **kwargs):
    """
    Full collaborative workflow with all features
    """
    orchestrator = CollaborativeOrchestrator()
    
    return orchestrator.run_comprehensive_workflow(
        student_answer=student_answer,
        sample_answer=sample_answer,
        concept=concept,
        create_curriculum=kwargs.get("create_curriculum", True),
        subject=kwargs.get("subject", concept),
        hours_per_day=kwargs.get("hours_per_day", 2),
        exam_date=kwargs.get("exam_date", "2025-12-15"),
        student_level=kwargs.get("student_level", "high school")
    )

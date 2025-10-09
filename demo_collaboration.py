"""
Demo script showcasing Multi-Agent Collaboration in EduMentorAI
Demonstrates how agents communicate and collaborate to provide better educational outcomes
"""

from agents.collaborative_orchestrator import CollaborativeOrchestrator
from agents.orchestrator import run_collaborative_workflow

def demo_basic_collaboration():
    """Demonstrate basic multi-agent collaboration"""
    print("=" * 80)
    print("🤖 EDUMENORAI MULTI-AGENT COLLABORATION DEMO")
    print("=" * 80)
    
    # Sample educational scenario
    student_answer = "Plants use sunlight to make food through a process."
    sample_answer = "Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to create glucose and oxygen."
    concept = "Photosynthesis"
    
    print("\n📚 EDUCATIONAL SCENARIO:")
    print(f"Concept: {concept}")
    print(f"Student Answer: '{student_answer}'")
    print(f"Expected Answer: '{sample_answer}'")
    print("\n" + "-" * 80)
    
    # Run collaborative workflow
    result = run_collaborative_workflow(
        student_answer=student_answer,
        sample_answer=sample_answer,
        concept=concept,
        create_curriculum=True,
        subject="Biology",
        hours_per_day=2,
        exam_date="2025-12-15"
    )
    
    # Display results
    print("\n📝 COLLABORATIVE RESULTS:")
    print("-" * 40)
    
    print("\n📖 CONCEPT EXPLANATION:")
    print(result.get("explanation", "Not available"))
    
    print("\n🔍 ASSESSMENT RESULTS:")
    print(result.get("assessment", "Not available"))
    
    print("\n💬 PERSONALIZED FEEDBACK:")
    print(result.get("feedback", "Not available"))
    
    if "curriculum_plan" in result:
        print("\n📅 ADAPTIVE CURRICULUM PLAN:")
        print(result.get("curriculum_plan", "Not available"))
    
    if "targeted_questions" in result:
        print("\n🎯 TARGETED PRACTICE QUESTIONS:")
        print(result.get("targeted_questions", "Not available"))
    
    # Show collaboration details
    print("\n" + "=" * 80)
    print("🤝 AGENT COLLABORATION SUMMARY")
    print("=" * 80)
    
    collaboration_summary = result.get("collaboration_summary", {})
    print(f"• Total Agent Messages: {collaboration_summary.get('total_agent_messages', 0)}")
    print(f"• Agents Participated: {', '.join(collaboration_summary.get('agents_participated', []))}")
    print(f"• Workflow Steps: {collaboration_summary.get('workflow_steps_completed', 0)}")
    print(f"• Context Data Shared: {collaboration_summary.get('context_data_shared', 0)} items")
    
    # Show agent interactions
    interactions = result.get("agent_interactions", [])
    if interactions:
        print("\n🔄 AGENT INTERACTIONS:")
        for i, interaction in enumerate(interactions[:5], 1):  # Show first 5 interactions
            print(f"{i}. {interaction['from']} → {interaction['to']} ({interaction['type']})")
            print(f"   Preview: {interaction['content_preview']}")
    
    return result

def demo_advanced_orchestrator():
    """Demonstrate advanced orchestrator capabilities"""
    print("\n" + "=" * 80)
    print("🚀 ADVANCED ORCHESTRATOR DEMO")
    print("=" * 80)
    
    orchestrator = CollaborativeOrchestrator()
    
    print("\n📊 AGENT STATUS:")
    agent_status = orchestrator.get_agent_status()
    for agent_id, status in agent_status.items():
        print(f"• {agent_id}: {status['specialization']} (Active: {status['active']})")
    
    print("\n📚 CURRICULUM PLANNING WORKFLOW:")
    curriculum_result = orchestrator.run_curriculum_planning_workflow(
        subject="Advanced Mathematics",
        hours_per_day=3,
        exam_date="2025-11-20",
        assessment_data={"weak_areas": ["calculus", "trigonometry"], "strong_areas": ["algebra"]}
    )
    
    print("Curriculum Plan Generated:")
    print(curriculum_result.get("curriculum_plan", "Not available")[:200] + "...")
    
    print("\n📝 ASSESSMENT GENERATION WORKFLOW:")
    assessment_result = orchestrator.run_assessment_workflow(
        topic="Calculus Derivatives",
        question_type="mixed",
        num_questions=3
    )
    
    print("Questions Generated:")
    print(assessment_result.get("exam_questions", "Not available")[:200] + "...")
    
    return orchestrator

def demo_agent_communication():
    """Demonstrate direct agent communication"""
    print("\n" + "=" * 80)
    print("💬 AGENT COMMUNICATION DEMO")
    print("=" * 80)
    
    orchestrator = CollaborativeOrchestrator()
    
    # Get agents
    subject_expert = orchestrator.agents["subject_expert"]
    assessment_agent = orchestrator.agents["assessment_agent"]
    
    print("\n🔄 Demonstrating Agent-to-Agent Communication:")
    
    # Subject expert requests assessment feedback
    print("1. Subject Expert requesting clarification from Assessment Agent...")
    message = subject_expert.send_message(
        "assessment_agent",
        {
            "task": "clarify_concept",
            "concept": "Photosynthesis",
            "aspect": "light-dependent reactions"
        },
        "collaboration_request"
    )
    
    if message:
        print(f"   ✅ Message sent: {message.id}")
    
    # Check inbox
    print(f"\n2. Assessment Agent inbox: {len(assessment_agent.inbox)} messages")
    
    # Show collaboration history
    print(f"3. Subject Expert collaborations: {len(subject_expert.collaboration_history)}")
    
    return orchestrator

if __name__ == "__main__":
    print("🎓 Starting EduMentorAI Multi-Agent Collaboration Demonstration")
    
    # Run basic collaboration demo
    basic_result = demo_basic_collaboration()
    
    # Run advanced orchestrator demo
    advanced_orchestrator = demo_advanced_orchestrator()
    
    # Run agent communication demo
    communication_orchestrator = demo_agent_communication()
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE - Multi-Agent Collaboration Successfully Demonstrated!")
    print("=" * 80)
    print("\n🔍 KEY FEATURES DEMONSTRATED:")
    print("• ✅ Agent-to-Agent Communication")
    print("• ✅ Shared Context Management") 
    print("• ✅ Collaborative Decision Making")
    print("• ✅ Adaptive Workflow Orchestration")
    print("• ✅ Context-Aware Educational Responses")
    print("• ✅ Multi-Step Collaborative Processing")
    
    print("\n🚀 Your EduMentorAI now has TRUE multi-agent collaboration!")
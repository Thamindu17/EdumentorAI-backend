from agents.orchestrator import run_workflow, run_collaborative_workflow
from agents.collaborative_orchestrator import CollaborativeOrchestrator

def demo_simple_workflow():
    """Demonstrate the enhanced simple workflow"""
    print("🔹 SIMPLE WORKFLOW DEMO")
    print("-" * 50)
    
    student_ans = "Plants take sunlight and make food from it."
    sample_ans = "Photosynthesis is how green plants use sunlight to turn water and carbon dioxide into food."
    concept = "Photosynthesis"

    result = run_workflow(student_ans, sample_ans, concept)

    print("\n📘 Explanation:\n", result["explanation"])
    print("\n🧠 Assessment:\n", result["assessment"])
    if "feedback" in result:
        print("\n💬 Feedback:\n", result["feedback"])
    
    if "collaboration_summary" in result:
        print("\n🤝 Collaboration Summary:")
        summary = result["collaboration_summary"]
        print(f"• Agents involved: {summary.get('agents_participated', [])}")
        print(f"• Messages exchanged: {summary.get('total_agent_messages', 0)}")

def demo_full_collaboration():
    """Demonstrate full collaborative workflow"""
    print("\n🔹 FULL COLLABORATIVE WORKFLOW DEMO")
    print("-" * 50)
    
    student_ans = "Cells divide to make new cells."
    sample_ans = "Mitosis is the process by which a single cell divides to produce two identical daughter cells, allowing organisms to grow and repair tissues."
    concept = "Cell Division"

    result = run_collaborative_workflow(
        student_answer=student_ans,
        sample_answer=sample_ans,
        concept=concept,
        create_curriculum=True,
        subject="Biology",
        hours_per_day=2.5,
        exam_date="2025-11-30",
        student_level="high school"
    )

    print("\n📘 Explanation:\n", result.get("explanation", "Not available"))
    print("\n🧠 Assessment:\n", result.get("assessment", "Not available"))
    print("\n💬 Feedback:\n", result.get("feedback", "Not available"))
    
    if "curriculum_plan" in result:
        print("\n📅 Curriculum Plan:\n", result["curriculum_plan"][:300] + "...")
    
    if "targeted_questions" in result:
        print("\n🎯 Targeted Questions:\n", result["targeted_questions"][:300] + "...")
    
    print("\n🤝 Collaboration Details:")
    collaboration = result.get("collaboration_summary", {})
    print(f"• Total agent interactions: {collaboration.get('total_agent_messages', 0)}")
    print(f"• Workflow steps completed: {collaboration.get('workflow_steps_completed', 0)}")
    print(f"• Context data items shared: {collaboration.get('context_data_shared', 0)}")

def demo_orchestrator_features():
    """Demonstrate advanced orchestrator features"""
    print("\n🔹 ORCHESTRATOR FEATURES DEMO")
    print("-" * 50)
    
    orchestrator = CollaborativeOrchestrator()
    
    # Show agent status
    print("\n📊 Agent Status:")
    status = orchestrator.get_agent_status()
    for agent_id, info in status.items():
        print(f"• {agent_id}: {info['specialization']}")
    
    # Demo curriculum planning
    print("\n📚 Curriculum Planning Workflow:")
    curriculum_result = orchestrator.run_curriculum_planning_workflow(
        subject="Python Programming",
        hours_per_day=3,
        exam_date="2025-12-01"
    )
    
    print("Curriculum generated:", curriculum_result["curriculum_plan"][:200] + "...")
    
    # Demo assessment generation
    print("\n📝 Assessment Generation Workflow:")
    assessment_result = orchestrator.run_assessment_workflow(
        topic="Object-Oriented Programming",
        question_type="mixed",
        num_questions=3
    )
    
    print("Questions generated:", assessment_result["exam_questions"][:200] + "...")

if __name__ == "__main__":
    print("🎓 EduMentorAI - Enhanced Multi-Agent Collaboration System")
    print("=" * 70)
    
    # Run simple workflow demo
    demo_simple_workflow()
    
    # Run full collaboration demo
    demo_full_collaboration()
    
    # Run orchestrator features demo
    demo_orchestrator_features()
    
    print("\n" + "=" * 70)
    print("✅ All demos completed successfully!")
    print("\n🚀 Key Enhancements Implemented:")
    print("• ✅ True agent-to-agent communication")
    print("• ✅ Shared context and memory")
    print("• ✅ Collaborative decision making")
    print("• ✅ Multi-step workflows")
    print("• ✅ Adaptive educational responses")
    print("• ✅ Context-aware feedback")
    print("\n🎯 Your EduMentorAI now has REAL multi-agent collaboration!")

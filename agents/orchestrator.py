from agents import assessment_agent, subject_expert

def run_workflow(student_answer, sample_answer, concept):
    explanation = subject_expert.explain_concept(concept)
    assessment = assessment_agent.assess_answer(student_answer, sample_answer)

    return {
        "explanation": explanation,
        "assessment": assessment
    }

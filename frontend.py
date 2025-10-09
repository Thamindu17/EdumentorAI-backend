import streamlit as st
from agents.orchestrator import run_collaborative_workflow, run_workflow
from agents.collaborative_orchestrator import CollaborativeOrchestrator

# Initialize session state
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = CollaborativeOrchestrator()

st.set_page_config(page_title="EduMentorAI", layout="wide")

st.title("EduMentorAI — Multi-Agent Educational Assistant")
st.markdown("Use this app to get explanations, assessments, feedback and adaptive study plans.")

mode = st.sidebar.selectbox("Mode", ["Simple", "Collaborative (Full)", "Question Generation"])

st.sidebar.header("Inputs")
concept = st.sidebar.text_input("Concept / Subject", value="Photosynthesis")
question_topic = None
question_type = None
num_questions = None

if mode == "Question Generation":
    question_topic = st.sidebar.text_input("Topic", value="Cell Division")
    question_type = st.sidebar.selectbox("Question Type", ["mixed", "mcq", "short answer", "essay"], index=0)
    num_questions = st.sidebar.number_input("Number of Questions", min_value=1, max_value=20, value=5, step=1)
else:
    student_answer = st.sidebar.text_area("Student Answer", value="Plants use sunlight to make food.")
    sample_answer = st.sidebar.text_area("Sample / Expected Answer", value="Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to create glucose and oxygen.")
    create_curriculum = st.sidebar.checkbox("Create curriculum plan", value=False)

if mode == "Collaborative (Full)":
    subject = st.sidebar.text_input("Subject (for curriculum)", value=concept)
    hours_per_day = st.sidebar.number_input("Hours per day", min_value=0.5, max_value=12.0, value=2.0, step=0.5)
    exam_date = st.sidebar.text_input("Exam date (YYYY-MM-DD)", value="2025-12-15")
    student_level = st.sidebar.selectbox("Student Level", ["elementary", "middle school", "high school", "college"], index=2)

show_raw = st.sidebar.checkbox("Show raw JSON result", value=False)

if st.sidebar.button("Run"):
    with st.spinner("Running agents..."):
        if mode == "Simple":
            result = run_workflow(student_answer, sample_answer, concept)
        elif mode == "Collaborative (Full)":
            result = run_collaborative_workflow(
                student_answer=student_answer,
                sample_answer=sample_answer,
                concept=concept,
                create_curriculum=create_curriculum,
                subject=subject,
                hours_per_day=hours_per_day,
                exam_date=exam_date,
                student_level=student_level
            )
        else:  # Question Generation mode
            # Use orchestrator directly for richer context capture
            questions_result = st.session_state.orchestrator.run_assessment_workflow(
                topic=question_topic,
                question_type=question_type,
                num_questions=num_questions
            )
            result = {"questions": questions_result.get("exam_questions"), **questions_result}

        st.session_state.last_result = result

if st.session_state.last_result:
    result = st.session_state.last_result
    if mode != "Question Generation":
        st.subheader("Explanation")
        st.write(result.get("explanation", "Not available"))

        st.subheader("Assessment")
        st.write(result.get("assessment", "Not available"))

        if result.get("feedback"):
            st.subheader("Feedback")
            st.write(result.get("feedback"))

        if result.get("curriculum_plan"):
            st.subheader("Curriculum Plan")
            st.write(result.get("curriculum_plan"))

        if result.get("targeted_questions"):
            st.subheader("Targeted Questions")
            st.write(result.get("targeted_questions"))
    else:
        st.subheader("Generated Questions")
        st.write(result.get("questions", "Not available"))

    if result.get("agent_interactions"):
        st.subheader("Agent Interactions")
        for msg in result.get("agent_interactions"):
            st.write(msg)

    if result.get("collaboration_summary"):
        st.subheader("Collaboration Summary")
        st.json(result.get("collaboration_summary"))

    if show_raw:
        st.subheader("Raw Result JSON")
        st.json(result)

st.sidebar.markdown("---")
st.sidebar.markdown("Powered by LangChain + LLM provider configured in agents/config.py")

from agents.orchestrator import run_workflow

if __name__ == "__main__":
    student_ans = "Plants take sunlight and make food from it."
    sample_ans = "Photosynthesis is how green plants use sunlight to turn water and carbon dioxide into food."
    concept = "Photosynthesis"

    result = run_workflow(student_ans, sample_ans, concept)

    print("\n📘 Explanation:\n", result["explanation"])
    print("\n🧠 Assessment:\n", result["assessment"])

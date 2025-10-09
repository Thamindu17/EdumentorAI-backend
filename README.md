# EduMentorAI

EduMentorAI is a multi-agent backend + lightweight Streamlit frontend that provides:

- Concept explanations
- Answer assessment & feedback
- Adaptive curriculum planning (optional)
- Exam / practice question generation
- Multi-agent collaboration (shared context + messaging)

It uses LangChain and configurable LLM providers (Groq or Hugging Face).

## Quick setup (local)

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure environment variables in a `.env` file at the project root. Example:

```
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_key
# or
LLM_PROVIDER=huggingface
HUGGINGFACEHUB_API_TOKEN=your_hf_token
```

4. Run the backend demos / API / frontend:

- To run the simple demo via CLI:

```powershell
python main.py
```

- To run the Streamlit frontend (includes Simple, Collaborative, and Question Generation modes):

```powershell
streamlit run frontend.py
```

- To run FastAPI server (for API routes):

```powershell
uvicorn app.main:app --reload --port 8000
```

## Streamlit Modes

| Mode | What it does | Function Called |
|------|---------------|-----------------|
| Simple | Concept explanation + assessment (+ feedback) | `run_workflow` (internally collaborative) |
| Collaborative (Full) | Full multi-step pipeline (explanation, assessment, feedback, optional curriculum, targeted questions) | `run_collaborative_workflow` |
| Question Generation | Generates exam/practice questions for a topic | `CollaborativeOrchestrator.run_assessment_workflow` |

Features:
- Optional curriculum plan (checkbox in Collaborative mode)
- Targeted questions appear when assessment indicates weaknesses
- Raw JSON toggle to inspect the entire response object
- Session caching preserves last result until next run

## Notes
- The project supports Groq and Hugging Face LLM providers. Configure your tokens in `.env`.
- The `demo_collaboration.py` shows multi-agent communication flows in detail.
- If `streamlit` import fails, make sure dependencies are installed in the active environment.
- Never commit real API keys—rotate them if accidentally exposed.

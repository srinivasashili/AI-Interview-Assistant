# 🎤 AI Interview Assistant

An interactive mock-interview tool built with **Python**, **Streamlit**, and the
**Anthropic Claude API**. Pick a target role, get AI-generated interview questions,
answer them, and receive instant structured feedback — scored and saved so you can
track progress over time.

## Features
- Role- and experience-level-specific question generation (behavioral, technical, scenario-based)
- Instant AI evaluation of answers: score (1-10), strengths, weaknesses, and a concrete improvement tip
- SQLite-backed session history with a score trend chart
- Clean, single-page Streamlit UI — no frontend code required

## Tech Stack
- **Python 3.10+**
- **Streamlit** — UI
- **Anthropic Claude API** — question generation & answer evaluation
- **SQLite** — local persistence
- **pandas** — history/trend charting

## Project Structure
```
ai-interview-assistant/
├── app.py                 # Main Streamlit app (UI + flow control)
├── prompts.py              # All LLM prompt templates, kept separate for easy tuning
├── llm_client.py            # Thin wrapper around the Anthropic API
├── db.py                    # SQLite persistence layer
├── requirements.txt
├── .streamlit/
│   └── secrets.toml.example  # Template for your API key
└── .gitignore
```

## Setup — Step by Step

### 1. Get an Anthropic API key
Go to [console.anthropic.com](https://console.anthropic.com), create an account,
and generate an API key from the API Keys section. Anthropic gives new accounts
a small free credit, which is enough for plenty of testing.

### 2. Clone/download this project and install dependencies
```bash
cd ai-interview-assistant
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API key
Rename `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste in your key:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```
This file is already in `.gitignore` — never commit your real key to GitHub.

### 4. Run the app locally
```bash
streamlit run app.py
```
It will open automatically at `http://localhost:8501`.

### 5. Try it out
- Enter a target role (e.g. "Python Backend Developer") in the sidebar
- Pick an experience level and number of questions
- Click **Start New Session**
- Answer each question, submit, and read the AI feedback
- Check the **History & Progress** tab to see your score trend over time

## Deployment (so you can share a live link with recruiters)

1. Push this project to a public GitHub repository (make sure `.streamlit/secrets.toml`
   is NOT included — only the `.example` file should be).
2. Go to [share.streamlit.io](https://share.streamlit.io) (Streamlit Community Cloud) and
   sign in with GitHub.
3. Click **New app**, select your repo, branch, and set the main file to `app.py`.
4. In the app's **Settings → Secrets**, paste the same content as your local
   `secrets.toml` (this is how Streamlit Cloud injects your API key securely).
5. Deploy. You'll get a public URL like `https://your-app-name.streamlit.app` —
   put this link directly on your resume/LinkedIn/GitHub README.

## Possible Extensions (good talking points in interviews)
- **Voice input**: record answers via mic, transcribe with Whisper API before evaluation
- **PDF resume parsing**: auto-generate questions tailored to a candidate's actual resume
- **Multi-user auth**: replace local SQLite with PostgreSQL + login, so it supports multiple users
- **Filler-word/fluency scoring**: analyze spoken answers for pacing and confidence signals

## Notes on Design Decisions
- Prompts are isolated in `prompts.py` and instruct the model to return strict JSON,
  which keeps the UI rendering predictable instead of parsing free-form text.
- `llm_client.py` defensively strips markdown fences before parsing JSON, since LLMs
  occasionally add them despite instructions not to — this kind of edge-case handling
  is exactly what's worth highlighting to a hiring manager.
- SQLite was chosen over a heavier database for simplicity; swapping it for PostgreSQL
  is a natural "next step" to mention if asked about scaling the project.

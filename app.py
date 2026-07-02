"""
AI Interview Assistant — Streamlit app.

Flow:
1. User picks a role + experience level.
2. App generates interview questions via Claude.
3. User answers each question (text input).
4. App evaluates each answer via Claude and shows structured feedback.
5. Everything is saved to SQLite so the user can review history/progress.
"""

import streamlit as st
import pandas as pd

import db
from prompts import question_generation_prompt, answer_evaluation_prompt
from llm_client import call_claude

st.set_page_config(page_title="AI Interview Assistant", page_icon="🎤", layout="centered")
db.init_db()

# ---------- Session state setup ----------
if "questions" not in st.session_state:
    st.session_state.questions = None
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

st.title("🎤 AI Interview Assistant")
st.caption("Practice real interview questions and get instant AI feedback on your answers.")

tab_practice, tab_history = st.tabs(["Practice", "History & Progress"])

# ================= PRACTICE TAB =================
with tab_practice:

    with st.sidebar:
        st.header("Setup")
        role = st.text_input("Target role", placeholder="e.g. Python Backend Developer")
        experience_level = st.selectbox(
            "Experience level",
            ["Entry-level / Fresher", "Mid-level (2-4 yrs)", "Senior (5+ yrs)"]
        )
        num_questions = st.slider("Number of questions", 3, 8, 5)

        if st.button("Start New Session", type="primary", use_container_width=True):
            if not role.strip():
                st.error("Please enter a target role first.")
            else:
                with st.spinner("Generating interview questions..."):
                    try:
                        result = call_claude(
                            question_generation_prompt(role, experience_level, num_questions)
                        )
                        st.session_state.questions = result["questions"]
                        st.session_state.session_id = db.create_session(role, experience_level)
                        st.session_state.current_index = 0
                        st.session_state.feedback_log = []
                        st.session_state.role = role
                    except Exception as e:
                        st.error(f"Failed to generate questions: {e}")

    if not st.session_state.questions:
        st.info("Fill in a role on the left and click **Start New Session** to begin.")
    else:
        questions = st.session_state.questions
        idx = st.session_state.current_index

        if idx < len(questions):
            q = questions[idx]
            st.subheader(f"Question {idx + 1} of {len(questions)}")
            st.markdown(f"**Type:** `{q['type']}`")
            st.markdown(f"> {q['question']}")

            answer = st.text_area("Your answer", key=f"answer_{idx}", height=180)

            if st.button("Submit Answer", type="primary"):
                if not answer.strip():
                    st.warning("Please write an answer before submitting.")
                else:
                    with st.spinner("Evaluating your answer..."):
                        try:
                            feedback = call_claude(
                                answer_evaluation_prompt(st.session_state.role, q["question"], answer)
                            )
                            db.save_answer(
                                st.session_state.session_id, q["question"], q["type"],
                                answer, feedback["score"], feedback
                            )
                            st.session_state.feedback_log.append(feedback)

                            st.success(f"Score: {feedback['score']}/10 — {feedback['summary']}")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Strengths**")
                                for s in feedback["strengths"]:
                                    st.markdown(f"- {s}")
                            with col2:
                                st.markdown("**Areas to improve**")
                                for w in feedback["weaknesses"]:
                                    st.markdown(f"- {w}")
                            st.info(f"💡 Tip: {feedback['improved_answer_tip']}")

                            st.session_state.current_index += 1
                            if st.session_state.current_index < len(questions):
                                if st.button("Next Question →"):
                                    st.rerun()
                            else:
                                st.balloons()
                                st.success("Session complete! Check the History tab for your full report.")
                        except Exception as e:
                            st.error(f"Failed to evaluate answer: {e}")
        else:
            st.success("✅ You've completed all questions in this session.")
            if st.session_state.feedback_log:
                avg = sum(f["score"] for f in st.session_state.feedback_log) / len(st.session_state.feedback_log)
                st.metric("Session average score", f"{avg:.1f} / 10")

# ================= HISTORY TAB =================
with tab_history:
    st.subheader("Practice History")

    history = db.get_score_history()
    if history:
        df = pd.DataFrame(history)
        df["created_at"] = pd.to_datetime(df["created_at"])
        st.line_chart(df.set_index("created_at")["score"])
    else:
        st.caption("No scored answers yet — complete a practice session to see trends here.")

    st.divider()
    sessions = db.get_all_sessions()
    if not sessions:
        st.caption("No sessions yet.")
    for s in sessions:
        with st.expander(f"{s['role']} ({s['experience_level']}) — {s['created_at'][:16]}"):
            answers = db.get_session_answers(s["id"])
            for a in answers:
                st.markdown(f"**Q:** {a['question']}")
                st.markdown(f"**Your answer:** {a['answer']}")
                st.markdown(f"**Score:** {a['score']}/10")
                st.divider()

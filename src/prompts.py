"""
Prompt templates for the AI Interview Assistant.
Keeping prompts in their own module makes them easy to test, version,
and tune independently of the application logic.
"""

def question_generation_prompt(role: str, experience_level: str, num_questions: int = 5) -> str:
    """
    Builds the prompt used to generate interview questions for a given role
    and experience level. Returns strict JSON so the app can parse it reliably.
    """
    return f"""You are an experienced technical interviewer at a top tech company.

Generate {num_questions} interview questions for a candidate applying for the role of "{role}"
at the "{experience_level}" experience level.

Requirements:
- Mix of question types: include at least one behavioral question, one conceptual/technical
  question, and one practical/scenario-based question.
- Questions should be realistic — the kind actually asked in real interviews, not generic
  textbook trivia.
- Calibrate difficulty to the experience level given.
- Do not include the answers.

Return ONLY valid JSON, no preamble, no markdown code fences, in exactly this format:
{{
  "questions": [
    {{"id": 1, "type": "behavioral", "question": "..."}},
    {{"id": 2, "type": "technical", "question": "..."}},
    {{"id": 3, "type": "scenario", "question": "..."}}
  ]
}}
"""


def answer_evaluation_prompt(role: str, question: str, answer: str) -> str:
    """
    Builds the prompt used to evaluate a candidate's answer to a single
    interview question. Returns strict JSON for consistent UI rendering.
    """
    return f"""You are an experienced technical interviewer evaluating a candidate's response
during a mock interview for the role of "{role}".

Question asked:
"{question}"

Candidate's answer:
"{answer}"

Evaluate the answer and return ONLY valid JSON, no preamble, no markdown code fences,
in exactly this format:
{{
  "score": <integer 1-10>,
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "improved_answer_tip": "One specific, actionable suggestion to make this answer stronger",
  "summary": "One sentence overall verdict"
}}

Scoring guide:
- 1-3: Off-topic, incorrect, or far too vague
- 4-6: Partially correct but missing structure, depth, or key points
- 7-8: Solid, correct, reasonably well-structured answer
- 9-10: Excellent — clear, structured, demonstrates strong expertise

If the answer is empty or just "I don't know", score it 1 and say so plainly in the summary.
"""

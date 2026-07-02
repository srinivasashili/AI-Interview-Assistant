import json
import re
import streamlit as st
from groq import Groq

MODEL = "llama-3.3-70b-versatile"

def get_api_key():
    api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None
    if not api_key:
        import os
        api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("No GROQ_API_KEY found.")
    return api_key

def _extract_json(text: str) -> dict:
    cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)

def call_claude(prompt: str, max_tokens: int = 1000) -> dict:
    client = Groq(api_key=get_api_key())
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content
    return _extract_json(text)
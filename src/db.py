"""
Simple SQLite persistence layer for storing practice sessions, questions,
answers, and feedback so users can review progress over time.
"""

import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "interview_assistant.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                question_type TEXT,
                answer TEXT NOT NULL,
                score INTEGER,
                feedback_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        """)


def create_session(role: str, experience_level: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO sessions (role, experience_level, created_at) VALUES (?, ?, ?)",
            (role, experience_level, datetime.utcnow().isoformat())
        )
        return cur.lastrowid


def save_answer(session_id: int, question: str, question_type: str,
                 answer: str, score: int, feedback: dict):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO answers
               (session_id, question, question_type, answer, score, feedback_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (session_id, question, question_type, answer, score,
             json.dumps(feedback), datetime.utcnow().isoformat())
        )


def get_all_sessions():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def get_session_answers(session_id: int):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM answers WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_score_history():
    """Returns (created_at, score) pairs across all sessions for trend charts."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT created_at, score FROM answers WHERE score IS NOT NULL ORDER BY created_at ASC"
        ).fetchall()
        return [dict(r) for r in rows]

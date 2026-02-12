import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    resume_path TEXT,
    resume_score REAL,
    status TEXT,
    interview_date TEXT,
    interview_link TEXT,
    interview_token TEXT
)
""")

conn.commit()
conn.close()

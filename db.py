import sqlite3
from typing import Optional
import datetime, os
DB_PATH = os.path.join(os.path.dirname(__file__), "plans.db")

def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal TEXT,
        created_on TEXT,
        start_date TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        title TEXT,
        duration_days INTEGER,
        earliest_start TEXT,
        latest_end TEXT,
        depends_on TEXT,
        notes TEXT,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    )
    """)
    conn.commit()
    conn.close()

def save_plan(plan):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO projects (goal, created_on, start_date) VALUES (?,?,?)",
                (plan.goal, plan.created_on.isoformat(), plan.start_date.isoformat()))
    pid = cur.lastrowid
    for t in plan.tasks:
        cur.execute("INSERT INTO tasks (project_id,title,duration_days,earliest_start,latest_end,depends_on,notes) VALUES (?,?,?,?,?,?,?)",
                    (pid,t.title,t.duration_days,t.earliest_start.isoformat() if t.earliest_start else None,
                     t.latest_end.isoformat() if t.latest_end else None,
                     ",".join(map(str,t.depends_on)), t.notes))
    conn.commit()
    conn.close()
    return pid

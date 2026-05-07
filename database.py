import sqlite3
import json

DB_NAME = "budget.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY,
        incomes TEXT,
        expenses TEXT,
        savings_entries TEXT,
        savings_boxes TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_user(user):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO users 
    (name, incomes, expenses, savings_entries, savings_boxes)
    VALUES (?, ?, ?, ?, ?)
    """, (
        user.name,
        json.dumps(user.incomes),
        json.dumps(user.expenses),
        json.dumps(user.savings_entries),
        json.dumps(user.savings_boxes)
    ))

    conn.commit()
    conn.close()


def load_user(name, User):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        user = User(row[0])
        user.incomes = json.loads(row[1]) if row[1] else []
        user.expenses = json.loads(row[2]) if row[2] else []
        user.savings_entries = json.loads(row[3]) if row[3] else []
        user.savings_boxes = json.loads(row[4]) if row[4] else []
        return user

    return None

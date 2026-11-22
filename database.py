import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "expenses.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_expense(date, category, description, amount):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (date, category, description, amount)
            VALUES (?, ?, ?, ?)
            """,
            (date, category, description, amount),
        )
        return cursor.lastrowid


def update_expense(expense_id, date, category, description, amount):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE expenses
            SET date = ?, category = ?, description = ?, amount = ?
            WHERE id = ?
            """,
            (date, category, description, amount, expense_id),
        )
        return cursor.rowcount


def delete_expense(expense_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,),
        )
        return cursor.rowcount


def get_expenses():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, date, category, description, amount "
            "FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_total_spending():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses"
        ).fetchone()
        return result["total"]


create_table()

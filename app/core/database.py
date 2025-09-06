"""
Database operations using SQLite
"""

import sqlite3
from typing import List, Optional
from app.models.reminder import Reminder

class DatabaseManager:
    """Manages database operations for reminders"""

    def __init__(self, db_path: str = "reminders.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS reminders
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     task TEXT NOT NULL,
                     time_str TEXT NOT NULL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        conn.commit()
        conn.close()

    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)

    def add_reminder(self, task: str, time_str: str) -> Optional[int]:
        """Add a new reminder to the database"""
        try:
            conn = self.get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO reminders (task, time_str) VALUES (?, ?)",
                     (task, time_str))
            reminder_id = c.lastrowid
            conn.commit()
            conn.close()
            return reminder_id
        except Exception as e:
            print(f"Error adding reminder: {e}")
            return None

    def get_all_reminders(self) -> List[Reminder]:
        """Retrieve all reminders from the database"""
        reminders = []
        try:
            conn = self.get_connection()
            c = conn.cursor()
            c.execute("SELECT id, task, time_str, created_at FROM reminders ORDER BY created_at DESC")

            for row in c.fetchall():
                reminders.append(Reminder(
                    id=row[0],
                    task=row[1],
                    time_str=row[2],
                    created_at=row[3]
                ))

            conn.close()
        except Exception as e:
            print(f"Error retrieving reminders: {e}")

        return reminders

    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder by ID"""
        try:
            conn = self.get_connection()
            c = conn.cursor()
            c.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting reminder: {e}")
            return False
# models/database.py
import sqlite3

class Database:
    def __init__(self, db_path: str = "users.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def create_user(self, name: str, login: str, password: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, login, password) VALUES (?, ?, ?)",
            (name, login, password)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_login(self, login: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        return cursor.fetchone()

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

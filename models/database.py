import sqlite3
from datetime import datetime


class Database:
    """Низкоуровневая работа с SQLite (без HTTP и шаблонов)"""

    def __init__(self, db_path: str = "notes.db"):
        # Подключение к SQLite-файлу в корне проекта
        self.conn = sqlite3.connect(db_path)
        # Чтобы получать dict-подобные строки: row["login"]
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Создание таблиц, если их ещё нет."""
        cur = self.conn.cursor()

        # Таблица пользователей
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                name     TEXT    NOT NULL,
                login    TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            );
        """)

        # Таблица заметок
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                title      TEXT    NOT NULL,
                text       TEXT    NOT NULL,
                created_at TEXT    NOT NULL,
                updated_at TEXT    NOT NULL,
                tags       TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        self.conn.commit()

    # ---------- USERS ----------

    def create_user(self, name: str, login: str, password: str) -> int:
        """Создать пользователя, вернуть его id."""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO users (name, login, password) VALUES (?, ?, ?)",
            (name, login, password),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_user_by_login(self, login: str):
        """Получить пользователя по логину"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE login = ?", (login,))
        return cur.fetchone()

    def get_all_users(self):
        """Список всех пользователей"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY id")
        return cur.fetchall()

    # ---------- NOTES ----------

    def create_note(self, user_id: int, title: str, text: str, tags: str | None = None) -> int:
        """Создать заметку для пользователя и вернуть id заметки."""
        now = datetime.now().isoformat(timespec="seconds")
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO notes (user_id, title, text, created_at, updated_at, tags)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, text, now, now, tags),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_user_notes(self, user_id: int):
        """Получить все заметки пользователя."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()

    def update_note(self, note_id: int, user_id: int,
                    title: str, text: str, tags: str | None = None) -> bool:
        """Обновить заметку (только свою). Вернуть True, если что-то изменено."""
        now = datetime.now().isoformat(timespec="seconds")
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE notes
               SET title = ?, text = ?, updated_at = ?, tags = ?
             WHERE id = ? AND user_id = ?
            """,
            (title, text, now, tags, note_id, user_id),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete_note(self, note_id: int, user_id: int) -> bool:
        """Удалить заметку (только свою)."""
        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?",
            (note_id, user_id),
        )
        self.conn.commit()
        return cur.rowcount > 0

    # ---------- SERVICE ----------

    def close(self) -> None:
        self.conn.close()

# controllers/notes_controller.py
from typing import Optional, List, Dict

from models.database import Database


class NotesController:
    """CRUD по заметкам пользователя поверх SQLite."""

    def __init__(self, db: Optional[Database] = None, db_path: str = "notes.db"):
        # Либо принимаем уже созданный Database, либо создаём свой
        self.db = db if db is not None else Database(db_path)

    def create_note(self, user_id: int, title: str, text: str, tags: str | None = None) -> int:
        """
        Создать заметку для пользователя.
        Возвращает id новой заметки.
        """
        if len(title.strip()) == 0:
            raise ValueError("Заголовок не может быть пустым")
        if len(text.strip()) == 0:
            raise ValueError("Текст заметки не может быть пустым")

        note_id = self.db.create_note(user_id, title.strip(), text.strip(), tags)
        return note_id

    def list_user_notes(self, user_id: int) -> List[Dict]:
        """
        Получить все заметки пользователя в виде списка словарей
        (удобно для передачи в шаблон).
        """
        rows = self.db.get_user_notes(user_id)
        notes = []
        for row in rows:
            notes.append({
                "id": row["id"],
                "user_id": row["user_id"],
                "title": row["title"],
                "text": row["text"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "tags": row["tags"],
            })
        return notes

    def update_note(self, note_id: int, user_id: int,
                    title: str, text: str, tags: str | None = None) -> bool:
        """
        Обновить заметку пользователя.
        Возвращает True, если заметка обновлена (и принадлежала этому user_id).
        """
        if len(title.strip()) == 0:
            raise ValueError("Заголовок не может быть пустым")
        if len(text.strip()) == 0:
            raise ValueError("Текст заметки не может быть пустым")

        return self.db.update_note(
            note_id=note_id,
            user_id=user_id,
            title=title.strip(),
            text=text.strip(),
            tags=tags,
        )

    def delete_note(self, note_id: int, user_id: int) -> bool:
        """
        Удалить заметку пользователя.
        True, если что‑то удалено.
        """
        return self.db.delete_note(note_id, user_id)

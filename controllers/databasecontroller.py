# controllers/database_controller.py
from typing import Optional

from models import User, UsersManager
from models.database import Database


class DatabaseController:
    """Бизнес-логика поверх SQLite-БД и моделей User/UsersManager."""

    def __init__(self, db_path: str = "notes.db"):
        # Подключение к SQLite через модель Database
        self.db = Database(db_path)
        # Удобный список пользователей в памяти (кеш)
        self.users = UsersManager()
        self._load_users_from_db()

    def _load_users_from_db(self) -> None:
        """Загрузить всех пользователей из БД в менеджер."""
        rows = self.db.get_all_users()
        for row in rows:
            # row["name"], row["login"], row["password"] — из SQLite
            user = User(row["name"], row["login"], row["password"])
            # UsersManager сам проверит тип и уникальность логина
            self.users.append(user)

    # ---------- Пользователи ----------

    def register_user(self, name: str, login: str, password: str) -> bool:
        """
        Регистрация нового пользователя:
        1) валидация User,
        2) запись в SQLite,
        3) добавление в кеш UsersManager.
        """
        # Проверка, что логин ещё не занят в БД
        if self.db.get_user_by_login(login) is not None:
            return False

        try:
            user = User(name, login, password)
            # 1) сохраняем в БД
            self.db.create_user(user.name, user.login, user.password)
            # 2) кладём в память
            self.users.append(user)
            return True
        except (ValueError, TypeError):
            return False

    def login_user(self, login: str, password: str) -> Optional[User]:
        """
        Вход пользователя через SQLite:
        1) берём запись из БД по логину,
        2) сравниваем пароль в открытую (если без хеша),
        3) создаём объект User при успехе.
        """
        row = self.db.get_user_by_login(login)
        if row is None:
            return None

        if row["password"] != password:
            return None

        return User(row["name"], row["login"], row["password"])

    def get_all_users(self) -> UsersManager:
        """Получить всех пользователей (кеш в памяти)."""
        return self.users

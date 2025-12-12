# controllers/database_controller.py
from typing import Optional
from models import UsersManager, User
from controllers.database import Database

class DatabaseController:
    def __init__(self, db_path: str = "users.db"):
        self.db = Database(db_path)      # ← связь с SQLite
        self.users = UsersManager()
        self._load_users_from_db()       # загружаем пользователей из БД

    def _load_users_from_db(self):
        """Загрузка пользователей из БД в менеджер."""
        rows = self.db.get_all_users()
        for row in rows:
            user = User(row["name"], row["login"], row["password"])
            self.users.append(user)

    def register_user(self, name: str, login: str, password: str) -> bool:
        """Регистрация нового пользователя (БД + память)."""
        # уже есть такой логин?
        if self.db.get_user_by_login(login) is not None:
            return False
        try:
            user = User(name, login, password)
            # 1) пишем в SQLite
            self.db.create_user(user.name, user.login, user.password)
            # 2) кладём в память
            self.users.append(user)
            return True
        except (ValueError, TypeError):
            return False

    def login_user(self, login: str, password: str) -> Optional[User]:
        """Вход пользователя через SQLite."""
        row = self.db.get_user_by_login(login)
        if row is None:
            return None
        # тут у тебя пароль в открытом виде, поэтому просто сравниваем
        if row["password"] != password:
            return None
        # создаём объект User (можно также искать в self.users)
        return User(row["name"], row["login"], row["password"])

    def get_all_users(self) -> UsersManager:
        """Получить всех пользователей (из памяти)."""
        return self.users

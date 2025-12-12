# controllers/database_controller.py
from models import UsersManager, User

class DatabaseController:
    def __init__(self):
        self.users = UsersManager()
        self._load_sample_users()

    def _load_sample_users(self):
        """Загрузка тестовых пользователей."""
        try:
            user1 = User("Иван Иванов", "ivan123", "pass123")
            user2 = User("Мария Петрова", "maria88", "secret88")
            self.users.extend([user1, user2])
        except ValueError as e:
            print(f"Ошибка загрузки пользователей: {e}")

    def register_user(self, name: str, login: str, password: str) -> bool:
        """Регистрация нового пользователя."""
        try:
            user = User(name, login, password)
            self.users.append(user)
            return True
        except (ValueError, TypeError):
            return False

    def login_user(self, login: str, password: str) -> Optional[User]:
        """Вход пользователя."""
        return self.users.authenticate(login, password)

    def get_all_users(self) -> UsersManager:
        """Получить всех пользователей."""
        return self.users

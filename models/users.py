from collections import UserList
from typing import Optional, List
from .user import User  # Импорт User из той же папки models


class UsersManager(UserList):
    """Менеджер для хранения и управления списком пользователей."""

    def __init__(self, users: Optional[List[User]] = None):
        """Инициализация с валидацией всех пользователей."""
        if users is None:
            users = []
        validated_users = []
        for user in users:
            if isinstance(user, User):
                validated_users.append(user)
            else:
                raise TypeError(f"Элемент {user} должен быть объектом User")
        super().__init__(validated_users)

    def append(self, user: User) -> None:
        """Добавление пользователя с проверкой уникальности логина."""
        if not isinstance(user, User):
            raise TypeError("Можно добавлять только объекты User")

        # Проверка уникальности логина
        if any(u.login == user.login for u in self):
            raise ValueError(f"Пользователь с логином '{user.login}' уже существует")

        super().append(user)

    def extend(self, users: List[User]) -> None:
        """Расширение списка пользователей."""
        for user in users:
            self.append(user)

    def authenticate(self, login: str, password: str) -> Optional[User]:
        """Аутентификация пользователя по логину и паролю."""
        for user in self:
            if user.login == login and user.password == password:
                return user
        return None

    def find_by_login(self, login: str) -> Optional[User]:
        """Поиск пользователя по логину."""
        for user in self:
            if user.login == login:
                return user
        return None

    def find_by_name(self, name: str) -> List[User]:
        """Поиск пользователей по имени."""
        return [user for user in self if user.name.lower() == name.lower()]

    def get_all_logins(self) -> List[str]:
        """Получить список всех логинов."""
        return [user.login for user in self]

    def delete_by_login(self, login: str) -> bool:
        """Удаление пользователя по логину."""
        for i, user in enumerate(self):
            if user.login == login:
                del self[i]
                return True
        return False


# test_users.py
from models import User, UsersManager

# Создание пользователей
users_mgr = UsersManager()

user1 = User("Админ", "admin", "admin123")
user2 = User("Пользователь", "user456", "pass456")

users_mgr.append(user1)
users_mgr.append(user2)

# Тесты
print(f"Пользователей: {len(users_mgr)}")
print(f"Логины: {users_mgr.get_all_logins()}")

# Аутентификация
admin = users_mgr.authenticate("admin", "admin123")
print(f"Авторизован: {admin.name if admin else 'не найден'}")

# Поиск
found = users_mgr.find_by_login("user456")
print(f"Найден: {found.login if found else 'не найден'}")

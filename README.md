# Лабораторная № 11: Приложение для заметок

## Развертывание проекта

1. Клонировать репозиторий:
```bash
git clone https://github.com/miurwur/lab11.git
```
2. Установить зависимости
```bash
pip install -r requirements.txt
```
3. Применить миграции:
```bash
python manage.py migrate
```
4. Создать суперпользователя:
```bash
python manage.py createsuperuser
```
5. Запустить сервер:
```bash
python manage.py runserver
```
6. Открыть в браузере: http://127.0.0.1:8000/

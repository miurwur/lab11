from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import os

from controllers.databasecontroller import DatabaseController
from controllers.notescontroller import NotesController

PORT = 8080
TEMPLATES_DIR = "templates"


def load_template(name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class RequestHandler(BaseHTTPRequestHandler):
    db_ctrl = DatabaseController("notes.db")
    notes_ctrl = NotesController(db_ctrl.db)

    def _send_html(self, html: str, status: int = 200):
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/":
            html = load_template("index.html")
            self._send_html(html)
        elif path == "/register":
            html = load_template("register.html")
            self._send_html(html)
        elif path == "/login":
            html = load_template("login.html")
            self._send_html(html)
        elif path == "/notes":
            # ожидаем ?user_id=1&login=ivan123
            user_id = int(params.get("user_id", ["0"])[0])
            user_login = params.get("login", ["unknown"])[0]
            notes = self.notes_ctrl.list_user_notes(user_id)

            tpl = load_template("notes_user.html")
            # очень примитивная подстановка вместо Jinja2
            items = ""
            for n in notes:
                items += f"<li><strong>{n['title']}</strong> ({n['created_at']})<br>{n['text']}<br>Теги: {n['tags']}</li>"

            html = tpl.replace("{{ user_login }}", user_login) \
                      .replace("{{ user_id }}", str(user_id)) \
                      .replace("{% for note in notes %}", "") \
                      .replace("{% endfor %}", "") \
                      .replace("{{ note.title }}", "") \
                      .replace("{{ note.created_at }}", "") \
                      .replace("{{ note.text }}", "") \
                      .replace("{{ note.tags }}", "") \
                      .replace("</ul>", items + "</ul>")
            self._send_html(html)
        else:
            self._send_html("<h1>404 Not Found</h1>", status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)

        if path == "/register":
            name = data.get("name", [""])[0]
            login = data.get("login", [""])[0]
            password = data.get("password", [""])[0]
            ok = self.db_ctrl.register_user(name, login, password)
            if ok:
                self._send_html("<p>Регистрация успешна. <a href=\"/login\">Войти</a></p>")
            else:
                self._send_html("<p>Ошибка регистрации (логин занят или некорректные данные).</p>")
        elif path == "/login":
            login = data.get("login", [""])[0]
            password = data.get("password", [""])[0]
            user = self.db_ctrl.login_user(login, password)
            if user is None:
                self._send_html("<p>Неверный логин или пароль.</p>")
            else:
                # в реальном приложении здесь должна быть сессия/кука
                self.send_response(302)
                self.send_header("Location", f"/notes?user_id=1&login={login}")
                self.end_headers()
        elif path == "/notes/create":
            user_id = int(data.get("user_id", ["0"])[0])
            title = data.get("title", [""])[0]
            text = data.get("text", [""])[0]
            tags = data.get("tags", [""])[0]
            self.notes_ctrl.create_note(user_id, title, text, tags)
            self.send_response(302)
            self.send_header("Location", f"/notes?user_id={user_id}")
            self.end_headers()
        elif path == "/notes/delete":
            user_id = int(data.get("user_id", ["0"])[0])
            note_id = int(data.get("note_id", ["0"])[0])
            self.notes_ctrl.delete_note(note_id, user_id)
            self.send_response(302)
            self.send_header("Location", f"/notes?user_id={user_id}")
            self.end_headers()
        else:
            self._send_html("<h1>404 Not Found</h1>", status=404)


def main():
    server = HTTPServer(("localhost", PORT), RequestHandler)
    print(f"Сервер запущен на http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        server.server_close()


if __name__ == "__main__":
    main()

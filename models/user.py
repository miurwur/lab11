class User():
    def __init__(self, name: str, login: str, password: str):
        # конструктор

        # Валидация при создании объекта
        if len(name) < 1:
            raise ValueError('Имя не может быть меньше 1 символа')
        if len(login) < 5:
            raise ValueError('Длина логина должна быть не меньше 5')
        if len(password) < 5:
            raise ValueError('Длина пароля должна быть не меньше 5')

        self.__name = name
        self.__login = login
        self.__password = password

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if len(name) >= 1:
            self.__name = name
        else:
            raise ValueError('Имя не может быть меньше 1 символа')

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login):
        if len(login) > 5:
            self.__login = login
        else:
            raise ValueError('Длина логина должна быть не меньше 5')

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if len(password) > 0:
            self.__password = password
        else:
            raise ValueError('Длина пароля должна быть не меньше 5')

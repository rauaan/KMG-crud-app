"""Инициализация расширений Flask.

Модуль содержит экземпляры расширений, используемых приложением.
Они создаются без привязки к приложению и инициализируются
в процессе создания Flask-приложения.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from faker import Faker
from flask_migrate import Migrate


#: Экземпляр SQLAlchemy для работы с базой данных.
db = SQLAlchemy()

#: Экземпляр Bcrypt для хеширования паролей пользователей.
bcrypt = Bcrypt()

#: Менеджер аутентификации пользователей.
login_manager = LoginManager()
login_manager.login_message = "Пожалуйста, войдите в систему."
login_manager.login_message_category = "warning"

#: Генератор тестовых данных на русском языке.
faker = Faker('ru_RU')

migrate = Migrate()
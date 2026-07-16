"""Конфигурация Flask-приложения.

Модуль содержит настройки приложения, загружаемые из переменных
окружения. Используется для конфигурации безопасности и подключения
к базе данных.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Базовая конфигурация Flask-приложения.

    Загружает секретный ключ приложения и параметры подключения
    к базе данных из переменных окружения.
    """

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

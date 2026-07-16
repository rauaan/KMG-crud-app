"""Пакет маршрутов приложения.

Модуль экспортирует все Blueprint-объекты, используемые
для регистрации маршрутов в Flask-приложении.
"""

from .auth import auth_bp
from .users import users_bp
from .companies import companies_bp
from .wells import wells_bp
from .daily_productions import daily_productions_bp


__all__ = [
    "auth_bp",
    "users_bp",
    "companies_bp",
    "wells_bp",
    "daily_productions_bp",
]
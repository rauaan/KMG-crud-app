"""Модели базы данных информационной системы нефтедобывающей компании.

Модуль содержит ORM-модели SQLAlchemy для хранения учетных записей,
сотрудников, нефтяных компаний, скважин и суточных производственных рапортов.
"""

from app.extensions import db
from flask_login import UserMixin


class Account(db.Model, UserMixin):
    """Модель учетной записи пользователя.

    Используется для аутентификации и авторизации пользователей системы.
    """

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class User(db.Model):
    """Модель сотрудника нефтяной компании.

    Каждый сотрудник принадлежит одной нефтяной компании.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    lName = db.Column(db.String(255), nullable=False)
    fName = db.Column(db.String(255), nullable=False)
    oil_company_id = db.Column(
        db.Integer,
        db.ForeignKey("oil_companies.id"),
        nullable=False,
    )

    company = db.relationship("Company", back_populates="users")


class Company(db.Model):
    """Модель нефтяной компании.

    Хранит информацию о компании и связанных с ней сотрудниках и скважинах.
    """

    __tablename__ = "oil_companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)

    users = db.relationship("User", back_populates="company")
    wells = db.relationship("Well", back_populates="company")


class Well(db.Model):
    """Модель нефтяной скважины.

    Каждая скважина принадлежит одной компании и содержит
    историю ежедневных производственных рапортов.
    """

    __tablename__ = "wells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    max_drilling_depth = db.Column(db.Float, nullable=False)
    oil_company_id = db.Column(
        db.Integer,
        db.ForeignKey("oil_companies.id"),
        nullable=False,
    )

    company = db.relationship("Company", back_populates="wells")
    daily_productions = db.relationship(
        "DailyProduction",
        back_populates="well",
    )


class DailyProduction(db.Model):
    """Модель суточного производственного рапорта.

    Один рапорт соответствует одной скважине за конкретную дату.
    Первичный ключ состоит из идентификатора скважины и даты.
    """

    __tablename__ = "daily_productions"

    well_id = db.Column(
        db.Integer,
        db.ForeignKey("wells.id"),
        primary_key=True,
        nullable=False,
    )
    date = db.Column(
        db.Date,
        primary_key=True,
        nullable=False,
    )

    operating_hours = db.Column(db.Float, nullable=False)
    liquid_produced = db.Column(db.Float, nullable=False)
    water_cut = db.Column(db.Float, nullable=False)
    density = db.Column(db.Float, nullable=False)

    well = db.relationship("Well", back_populates="daily_productions")

    @property
    def net_oil(self):
        """Вычисляет объем чистой нефти в тоннах.

        Расчет выполняется по формуле:

            Жидкость × (1 − Обводненность / 100) × Плотность.

        Returns:
            float: Объем чистой нефти в тоннах.
        """
        return self.liquid_produced * (1 - self.water_cut / 100) * self.density

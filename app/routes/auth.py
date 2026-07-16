"""Маршруты аутентификации пользователей.

Модуль содержит обработчики запросов для регистрации,
авторизации и выхода пользователей из системы.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from app.extensions import db, bcrypt, login_manager
from app.models import Account
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    """Загружает пользователя по его идентификатору.

    Используется Flask-Login для восстановления информации
    об авторизованном пользователе из сессии.

    Args:
        user_id: Идентификатор пользователя.

    Returns:
        Account | None: Найденный пользователь или None.
    """
    return db.session.get(Account, int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Выполняет авторизацию пользователя.

    При GET-запросе отображает форму входа.
    При POST-запросе проверяет введенные учетные данные
    и выполняет вход в систему.

    Returns:
        Response: Форма входа или перенаправление
        на главную страницу после успешной авторизации.
    """

    form = LoginForm()

    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account)

            next_page = request.args.get("next")

            return redirect(next_page or url_for("index"))

        flash("Неверное имя пользователя или пароль.", "warning")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Регистрирует нового пользователя.

    При GET-запросе отображает форму регистрации.
    При POST-запросе создает новую учетную запись,
    предварительно хешируя пароль.

    Returns:
        Response: Форма регистрации или перенаправление
        на страницу входа после успешной регистрации.
    """

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_account = Account(username=form.username.data, password=hashed_password)
        try:
            db.session.add(new_account)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"ERROR {e}"

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """Завершает пользовательскую сессию.

    Выполняет выход пользователя из системы и
    перенаправляет его на страницу авторизации.

    Returns:
        Response: Перенаправление на страницу входа.
    """

    logout_user()
    return redirect(url_for("auth.login"))

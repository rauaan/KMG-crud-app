"""Маршруты для управления сотрудниками.

Модуль содержит обработчики запросов для просмотра, создания,
редактирования и удаления сотрудников.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.extensions import db
from app.models import User, Company

users_bp = Blueprint("users", __name__)


@users_bp.route("/")
@login_required
def users():
    """Отображает список сотрудников.

    Получает всех сотрудников из базы данных и передает
    их в HTML-шаблон для отображения.

    Returns:
        Response: Страница со списком сотрудников.
    """
    if request.method == "GET":
        employees = User.query.all()
    return render_template("main/index.html", employees=employees, company = Company)  


@users_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_employee():
    """Создает нового сотрудника.

    При GET-запросе отображает форму создания сотрудника.
    При POST-запросе сохраняет нового сотрудника в базе данных.

    Returns:
        Response: Форма создания или перенаправление
        к списку сотрудников.
    """

    if request.method == "POST":
        new_user = User(
            lName = request.form['lName'],
            fName = request.form['fName'],
            oil_company_id = request.form['company_id']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("users.users"))
        except Exception:
            db.session.rollback()
            return "ERROR Нет компании с таким id"

    return render_template(
        "main/create_user.html",
        employee=None,
        title="Добавить сотрудника",
        button_text="Создать")
    

@users_bp.route("/edit/<int:id>", methods=["GET", "POST"])  
@login_required
def edit_employee(id):
    """Редактирует информацию о сотруднике.

    При GET-запросе отображает форму редактирования.
    При POST-запросе сохраняет изменения в базе данных.

    Args:
        id: Идентификатор редактируемого сотрудника.

    Returns:
        Response: Форма редактирования или перенаправление
        к списку сотрудников после успешного сохранения.
    """
    
    to_edit = User.query.get_or_404(id)
    if request.method == "POST":
        to_edit.lName = request.form['lName']
        to_edit.fName = request.form['fName']
        to_edit.oil_company_id = request.form['company_id']
        
        try:
            db.session.commit()
            return redirect(url_for("users.users"))

        except Exception as e:
            return f"ERROR {e}"
    else:     
        return render_template(
            "main/create_user.html",
            employee=to_edit,
            title="Редактировать сотрудника",
            button_text="Сохранить"
        )


@users_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_employee(id:int):
    """Удаляет сотрудника из базы данных.

    Args:
        id: Идентификатор удаляемого сотрудника.

    Returns:
        Response: Перенаправление к списку сотрудников.
    """
    to_delete = User.query.get_or_404(id)
    
    try: 
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for("users.users"))
    except Exception as e:
        return f"ERROR {e}"
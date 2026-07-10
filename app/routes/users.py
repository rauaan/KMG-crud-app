from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import User, Company
from flask_login import login_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/")
@login_required
def users():
    if request.method == "GET":
        employees = User.query.all()
    return render_template("main/index.html", employees=employees, company = Company)  


@users_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_employee():

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
        except Exception as e:
            db.session.rollback()
            return f"ERROR Нет компании с таким id"

    return render_template(
        "main/create_user.html",
        employee=None,
        title="Добавить сотрудника",
        button_text="Создать")
    

@users_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_employee(id:int):
    to_delete = User.query.get_or_404(id)
    
    try: 
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for("users.users"))
    except Exception as e:
        return f"ERROR {e}"


@users_bp.route("/edit/<int:id>", methods=["GET", "POST"])  
@login_required
def edit_employee(id):
    to_edit = User.query.get_or_404(id)
    if request.method == "POST":
        to_edit.lName = request.form['lName']
        to_edit.fName = request.form['fName'],
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


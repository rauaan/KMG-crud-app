from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Company

companies_bp = Blueprint("companies", __name__)


@companies_bp.route("/")
@login_required
def companies():
    if request.method == "GET":
        companies = Company.query.all()
    return render_template("main/list_companies.html", companies=companies)  

@companies_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_company():

    if request.method == "POST":
        new_company = Company(
            name = request.form['name'],
            region = request.form['region']
        )
        try:
            db.session.add(new_company)
            db.session.commit()
            return redirect(url_for("companies.companies"))
        except Exception as e:
            db.session.rollback()
            return f"ERROR{e}"
    
    return render_template(
        "main/create_company.html",
        company=None,
        title="Добавить компанию",
        button_text="Создать")

@companies_bp.route("/edit/<int:id>", methods = ["GET", "POST"])
@login_required
def edit_company(id:int):
    to_edit = Company.query.get_or_404(id)
    if request.method == "POST":
        to_edit.name = request.form['name']
        to_edit.region = request.form['region']
        
        try:
            db.session.commit()
            return redirect(url_for("companies.companies"))

        except Exception as e:
            return f"ERROR {e}"
    else:     
        return render_template(
            "main/create_company.html",
            company=to_edit,
            title="Редактировать компанию",
            button_text="Сохранить"
        )
    
@companies_bp.route("/delete/<int:id>", methods = ["POST"])
@login_required
def delete_company(id:int):
    to_delete = Company.query.get_or_404(id)
    
    try: 
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for("companies.companies"))
    except Exception as e:
        return f"ERROR {e}"
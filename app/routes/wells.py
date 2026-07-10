from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Well, Company
from flask_login import login_required

wells_bp = Blueprint("wells", __name__)


@wells_bp.route("/")
@login_required
def wells():
    if request.method == "GET":
        wells = Well.query.all()
    return render_template("main/list_wells.html", wells = wells, company = Company)  

@wells_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_well():

    if request.method == "POST":
        new_well = Well(

            name = request.form['name'],
            type = request.form['type'],
            max_drilling_depth = request.form['max_drilling_depth'],
            oil_company_id = request.form['company_id']
        )
        try:
            db.session.add(new_well)
            db.session.commit()
            return redirect(url_for("wells.wells"))
        except Exception as e:
            db.session.rollback()
            return f"ERROR Нет компании с таким id"

    return render_template(
        "main/create_well.html",
        well=None,
        title="Добавить скважину",
        button_text="Создать")

@wells_bp.route("/edit/<int:id>", methods = ["GET", "POST"])
@login_required
def edit_well(id:int):
    to_edit = Well.query.get_or_404(id)
    if request.method == "POST":
        to_edit.name = request.form['name']
        to_edit.type = request.form['type']
        to_edit.max_drilling_depth = request.form['max_drilling_depth']
        to_edit.oil_company_id = request.form['company_id']
        
        try:
            db.session.commit()
            return redirect(url_for("wells.wells"))

        except Exception as e:
            return f"ERROR {e}"
    else:     
        return render_template(
            "main/create_well.html",
            well=to_edit,
            title="Редактировать скважину",
            button_text="Сохранить"
        )
    
@wells_bp.route("/delete/<int:id>", methods = ["POST"])
@login_required
def delete_well(id:int):
    to_delete = Well.query.get_or_404(id)
    
    try: 
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for("wells.wells"))
    except Exception as e:
        return f"ERROR {e}"
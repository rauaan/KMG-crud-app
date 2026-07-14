from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models import DailyProduction
from app.forms import CreateDailyProduction

daily_productions_bp = Blueprint("daily_productions", __name__)


@daily_productions_bp.route("/")
@login_required
def daily_productions():
    if request.method == "GET":
        reports = DailyProduction.query.all()
    return render_template("main/list_daily_productions.html", reports=reports)  


@daily_productions_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_daily_production():

    form = CreateDailyProduction()
    if request.method == "POST":
        if form.validate_on_submit():

            new_daily_production = DailyProduction(
                well_id = form.well_id.data,
                date = form.date.data,
                operating_hours = form.operating_hours.data,
                liquid_produced = form.liquid_produced.data,
                water_cut = form.water_cut.data,
                density = form.density.data
            )
            try:
                db.session.add(new_daily_production)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return f"ERROR{e}"

            return redirect(url_for("daily_productions.daily_productions"))

        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "warning")

    return render_template(
        "main/create_daily_production.html",
        form = form,
        title="Создать рапорт",
        button_text="Создать")


@daily_productions_bp.route("/edit/<int:well_id>/<date>", methods=["GET", "POST"])
@login_required
def edit_daily_production(well_id, date):
    report = DailyProduction.query.filter_by(
        well_id=well_id,
        date=date
    ).first_or_404()

    form = CreateDailyProduction(obj=report)

    if form.validate_on_submit():

        report.well_id = form.well_id.data
        report.date = form.date.data
        report.operating_hours = form.operating_hours.data
        report.liquid_produced = form.liquid_produced.data
        report.water_cut = form.water_cut.data
        report.density = form.density.data

        try:
            db.session.commit()
            return redirect(url_for("daily_productions.daily_productions"))

        except Exception as e:
            db.session.rollback()
            return f"ERROR {e}"

    else:
        for errors in form.errors.values():
            for error in errors:
                flash(error, "warning")

    return render_template(
        "main/create_daily_production.html",
        form=form,
        title="Редактировать рапорт",
        button_text="Сохранить"
    )
    
@daily_productions_bp.route("/delete/<int:well_id>/<date>", methods = ["POST"])
@login_required
def delete_daily_productionn(well_id, date):
    to_delete = DailyProduction.query.filter_by(
            well_id=well_id,
            date=date
        ).first_or_404()
    
    try: 
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for("daily_productions.daily_productions"))
    
    except Exception as e:
        return f"ERROR {e}"
from flask import Blueprint, render_template, request
from sqlalchemy import func

from app import db
from app.models import Company, Well, DailyProduction

dashboards_bp = Blueprint("dashboards", __name__)


@dashboards_bp.route("/")
def dashboards():

    # -----------------------------
    # Filters
    # -----------------------------

    company_id = request.args.get("company_id", type=int)
    well_id = request.args.get("well_id", type=int)

    companies = Company.query.order_by(Company.name).all()

    wells_query = Well.query.order_by(Well.name)

    if company_id:
        wells_query = wells_query.filter(
            Well.oil_company_id == company_id
        )

    wells = wells_query.all()

    # -----------------------------
    # Base query
    # -----------------------------

    production_query = (
        db.session.query(DailyProduction)
        .join(Well)
    )

    if company_id:
        production_query = production_query.filter(
            Well.oil_company_id == company_id
        )

    if well_id:
        production_query = production_query.filter(
            DailyProduction.well_id == well_id
        )

    # -----------------------------
    # KPI Cards
    # -----------------------------

    companies_count = Company.query.count()

    wells_count = (
        Well.query.filter_by(oil_company_id=company_id).count()
        if company_id
        else Well.query.count()
    )

    reports_count = production_query.count()

    total_net_oil = (
        production_query.with_entities(
            func.sum(
                DailyProduction.liquid_produced *
                (1 - DailyProduction.water_cut / 100.0)
            )
        ).scalar() or 0
    )

    avg_water_cut = (
        production_query.with_entities(
            func.avg(DailyProduction.water_cut)
        ).scalar() or 0
    )

    avg_liquid = (
        production_query.with_entities(
            func.avg(DailyProduction.liquid_produced)
        ).scalar() or 0
    )

    # -----------------------------
    # Top producing company
    # -----------------------------

    top_company = (
        db.session.query(
            Company.name,
            func.sum(
                DailyProduction.liquid_produced *
                (1 - DailyProduction.water_cut / 100.0)
            ).label("oil")
        )
        .join(Well, Well.oil_company_id == Company.id)
        .join(DailyProduction, DailyProduction.well_id == Well.id)
        .group_by(Company.id)
        .order_by(func.sum(
            DailyProduction.liquid_produced *
            (1 - DailyProduction.water_cut / 100.0)
        ).desc())
        .first()
    )

    top_company_name = top_company.name if top_company else "-"
    top_company_oil = float(top_company.oil) if top_company else 0

    # -----------------------------
    # Top producing well
    # -----------------------------

    top_well = (
        db.session.query(
            Well.name,
            func.sum(
                DailyProduction.liquid_produced *
                (1 - DailyProduction.water_cut / 100.0)
            ).label("oil")
        )
        .join(DailyProduction)
        .group_by(Well.id)
        .order_by(func.sum(
            DailyProduction.liquid_produced *
            (1 - DailyProduction.water_cut / 100.0)
        ).desc())
        .first()
    )

    top_well_name = top_well.name if top_well else "-"
    top_well_oil = float(top_well.oil) if top_well else 0

    # -----------------------------
    # Production over time
    # -----------------------------

    production = (
        production_query.with_entities(
            DailyProduction.date,
            func.sum(
                DailyProduction.liquid_produced *
                (1 - DailyProduction.water_cut / 100.0)
            )
        )
        .group_by(DailyProduction.date)
        .order_by(DailyProduction.date)
        .all()
    )

    production_labels = [
        row.date.strftime("%d.%m.%Y")
        for row in production
    ]

    production_values = [
        float(row[1])
        for row in production
    ]

    # -----------------------------
    # Average water cut by well
    # -----------------------------

    water = (
        production_query.with_entities(
            Well.name,
            func.avg(DailyProduction.water_cut)
        )
        .group_by(Well.id)
        .order_by(Well.name)
        .all()
    )

    water_labels = [
        row[0]
        for row in water
    ]

    water_values = [
        float(row[1])
        for row in water
    ]

    # -----------------------------
    # Well type distribution
    # -----------------------------

    well_type_query = db.session.query(
        Well.type,
        func.count(Well.id)
    )

    if company_id:
        well_type_query = well_type_query.filter(
            Well.oil_company_id == company_id
        )

    if well_id:
        well_type_query = well_type_query.filter(
            Well.id == well_id
        )

    well_types = (
        well_type_query
        .group_by(Well.type)
        .all()
    )

    well_type_labels = [
        row[0]
        for row in well_types
    ]

    well_type_values = [
        row[1]
        for row in well_types
    ]

    # -----------------------------
    # Production by company
    # -----------------------------

    company_data = (
        db.session.query(
            Company.id,
            Company.name,
            func.sum(
                DailyProduction.liquid_produced *
                (1 - DailyProduction.water_cut / 100.0)
            ).label("oil")
        )
        .join(Well, Well.oil_company_id == Company.id)
        .join(DailyProduction, DailyProduction.well_id == Well.id)
        .group_by(Company.id)
        .order_by(Company.name)
        .all()
    )

    company_ids = [
        row.id
        for row in company_data
    ]

    company_labels = [
        row.name
        for row in company_data
    ]

    company_values = [
        float(row.oil or 0)
        for row in company_data
    ]

    # -----------------------------
    # Production by well
    # -----------------------------

    well_production = (
        production_query.with_entities(
            Well.id,
            Well.name,
            func.sum(
                DailyProduction.liquid_produced *
                (1 - DailyProduction.water_cut / 100.0)
            ).label("oil")
        )
        .group_by(Well.id)
        .order_by(Well.name)
        .all()
    )

    well_ids = [
        row.id
        for row in well_production
    ]

    well_labels = [
        row.name
        for row in well_production
    ]

    well_values = [
        float(row.oil or 0)
        for row in well_production
    ]

    # -----------------------------
    # Render
    # -----------------------------

    return render_template(
        "main/dashboards.html",

        # filters
        companies=companies,
        wells=wells,
        selected_company=company_id,
        selected_well=well_id,

        # KPI cards
        companies_count=companies_count,
        wells_count=wells_count,
        reports_count=reports_count,
        total_net_oil=total_net_oil,
        avg_water_cut=avg_water_cut,
        avg_liquid=avg_liquid,

        top_company_name=top_company_name,
        top_company_oil=top_company_oil,

        top_well_name=top_well_name,
        top_well_oil=top_well_oil,

        # Production trend
        production_labels=production_labels,
        production_values=production_values,

        # Water cut
        water_labels=water_labels,
        water_values=water_values,

        # Well types
        well_type_labels=well_type_labels,
        well_type_values=well_type_values,

        # Company production
        company_ids=company_ids,
        company_labels=company_labels,
        company_values=company_values,

        # Well production
        well_ids=well_ids,
        well_labels=well_labels,
        well_values=well_values,
    )
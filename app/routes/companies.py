from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Company

companies_bp = Blueprint("companies", __name__)


@companies_bp.route("/")
def companies():
    if request.method == "GET":
        companies = Company.query.all()
    return render_template("main/index.html", employees=companies)  
from app.extensions import db
from flask_login import UserMixin


class Account(db.Model, UserMixin):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    lName = db.Column(db.String(255), nullable = False)
    fName = db.Column(db.String(255), nullable = False)
    oil_company_id = db.Column(db.Integer, db.ForeignKey("oil_companies.id"), nullable = False)

    company = db.relationship("Company", back_populates = "users")



class Company(db.Model):
    __tablename__ = "oil_companies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    region = db.Column(db.String(255), nullable = False)

    users = db.relationship("User", back_populates="company")
    wells = db.relationship("Well", back_populates="company")


class Well(db.Model):
    __tablename__ = "wells"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    type = db.Column(db.String(255), nullable = False)
    max_drilling_depth = db.Column(db.Float, nullable = False)
    oil_company_id = db.Column(db.Integer, db.ForeignKey("oil_companies.id"), nullable = False)

    company = db.relationship("Company", back_populates = "wells")
    daily_productions = db.relationship("DailyProduction", back_populates="well")


class DailyProduction(db.Model):
    __tablename__ = "daily_productions"

    well_id = db.Column(db.Integer, db.ForeignKey("wells.id"), primary_key=True, nullable = False)
    date = db.Column(db.Date, primary_key=True, nullable = False)

    operating_hours = db.Column(db.Float, nullable=False) #время работы
    liquid_produced = db.Column(db.Float, nullable=False) 
    water_cut = db.Column(db.Float, nullable=False) #обводенность
    density = db.Column(db.Float, nullable=False)   

    well = db.relationship("Well", back_populates = "daily_productions")

    @property
    def net_oil(self):
        return self.liquid_produced * (1 - self.water_cut / 100) * self.density
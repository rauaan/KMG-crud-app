from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    lName = db.Column(db.String(255), nullable = False)
    fName = db.Column(db.String(255), nullable = False)
    # oil_company_id = db.Column(db.Integer, db.ForeignKey("oil_companies.id"), nullable = False)


class Company(db.Model):
    __tablename__ = "oil_companies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    region = db.Column(db.String(255), nullable = False)


class Well(db.Model):
     __tablename__ = "wells"

     id = db.Column(db.Integer, primary_key = True)
     name = db.Column(db.String(255), nullable = False)
     type = db.Column(db.String(255), nullable = False)
     max_drilling_depth = db.Column(db.Integer, nullable = False)
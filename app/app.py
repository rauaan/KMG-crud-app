from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import io
from extensions import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/KMG-T2"
)

db.init_app(app)
from routes.users import users_bp
from routes.companies import companies_bp
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(companies_bp, url_prefix="/companies")

@app.route('/', methods=["GET"])
def index():

    return render_template("base.html")


@app.route("/upload", methods=["POST"])
def upload():
    global employees

    # file = request.files["excel_file"]

    # df = pd.read_excel(file)
    # employees = df.to_dict(orient="records")

    return render_template(
        "main/index.html",
        employees=employees
    )

@app.route("/download", methods=["GET"])
def download():
    df = pd.DataFrame(employees)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='file.xlsx'
    )


@app.route("/login")
def login():
    return render_template("auth/login.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
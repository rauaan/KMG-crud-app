from flask import Flask, render_template
import pandas as pd
from extensions import db, bcrypt, login_manager
from dotenv import load_dotenv
from config import Config
from flask_login import login_required

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login"

from routes.auth import auth_bp
from routes.users import users_bp
from routes.companies import companies_bp
from routes.wells import wells_bp

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(companies_bp, url_prefix="/companies")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(wells_bp, url_prefix="/wells")

@app.route('/', methods=["GET"])
@login_required
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
    return
    # df = pd.DataFrame(employees)
    # buffer = io.BytesIO()
    # with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    #     df.to_excel(writer, sheet_name='Sheet1', index=False)
        
    # buffer.seek(0)
    
    # return send_file(
    #     buffer,
    #     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #     as_attachment=True,
    #     download_name='file.xlsx'
    # )



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
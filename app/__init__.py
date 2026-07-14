from flask import Flask, render_template
from flask_login import login_required

from app.extensions import db, bcrypt, login_manager
from app.config import Config
from app.seed import make_data

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    from app.routes import auth_bp, users_bp, companies_bp, wells_bp, daily_productions_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(companies_bp, url_prefix="/companies")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(wells_bp, url_prefix="/wells")
    app.register_blueprint(daily_productions_bp, url_prefix="/daily_productions")

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

    app.cli.add_command(make_data)

    with app.app_context():
        db.create_all()

    return app
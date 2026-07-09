from flask import Blueprint, render_template, redirect, url_for, request, flash
from forms import LoginForm, RegistrationForm
from extensions import db, bcrypt, login_manager
from models import Account
from flask_login import login_user, login_required, logout_user

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        account = Account.query.filter_by(username = form.username.data).first()
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account)

            next_page = request.args.get("next")

            return redirect(next_page or url_for("index"))
        
        flash("Неверное имя пользователя или пароль.", "warning")


    return render_template("auth/login.html", form = form)

@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_account = Account(username = form.username.data, password = hashed_password)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template("auth/register.html", form = form)


@auth_bp.route("/logout", methods =  ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
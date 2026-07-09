from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import Account

class RegistrationForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Зарегистрироваться")

    def validate_username(self, username):
        existing_username = Account.query.filter_by(username = username.data).first()

        if existing_username:
            raise ValidationError("Имя пользователя уже существует")


class LoginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Войти")

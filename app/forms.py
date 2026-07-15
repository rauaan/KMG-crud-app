from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from app.models import Account, DailyProduction

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


class CreateDailyProduction(FlaskForm):
    well_id = IntegerField(validators= [InputRequired()])
    date = DateField(validators= [InputRequired()])

    operating_hours = IntegerField(validators= [InputRequired(), NumberRange(min=0, max=24, message = "время работы 0-24ч")])
    liquid_produced = IntegerField(validators= [InputRequired()])
    water_cut = IntegerField(validators= [InputRequired(), NumberRange(min=0, max=100, message = "обводненность 0-100%%")])
    density = IntegerField(validators= [InputRequired()])

    def __init__(self, *args, original_well_id=None, original_date=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.original_well_id = original_well_id
            self.original_date = original_date

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        existing_report = DailyProduction.query.filter_by(
            well_id=self.well_id.data,
            date=self.date.data
        ).first()

        is_updating_same_record = (
                    self.original_well_id is not None and 
                    self.original_date is not None and
                    self.well_id.data == self.original_well_id and
                    self.date.data == self.original_date
                )
        
        if is_updating_same_record:
            return True

        if existing_report:
            self.date.errors.append(
                "Рапорт за этот день уже существует."
            )
            return False

        return True
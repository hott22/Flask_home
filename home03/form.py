from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    user_name = StringField('Имя', validators=[DataRequired()])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_birthday = DateField('Дата рождения', validators=[DataRequired()])
    user_password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    user_confirm_password = PasswordField('Повторить пароль', validators=[DataRequired(), EqualTo('user_password')])
    approval = BooleanField('Согласие на обработку персональных данных')
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин/Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Фамилия пользователя', validators=[DataRequired()])
    surname = StringField('Имя пользователя', validators=[DataRequired()])
    age = IntegerField('', validators=[])
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Специализация', validators=[DataRequired()])
    address = StringField('адрес', validators=[DataRequired()])
    submit = SubmitField('Войти')
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from wtforms import PasswordField, SubmitField, StringField, validators
from sqlalchemy import select

from ..db import User, db_manager



class RegisterForm(FlaskForm):
    name = StringField(
        'Имя', validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=150, message='Максимальное кол-во символов -- 150'),
        ],
    )

    password = PasswordField(
        'Пароль', validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=8, message='Минимальная длинна пароля - 8')
        ]
    )

    password_confirm = PasswordField(
        'Повторите пароль', validators=[
            DataRequired(message='Обязательное поле'),
            EqualTo('password', message='Пароли не совпадают')
        ]
    )

    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    name = StringField(
        'Имя', validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=150, message='Максимальное кол-во символов -- 150'),
        ],
    )

    password = PasswordField(
        'Пароль', validators=[
            DataRequired(message='Обязательное поле'),
        ]
    )
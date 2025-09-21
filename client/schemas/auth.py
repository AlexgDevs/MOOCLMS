from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from wtforms import PasswordField, SubmitField, StringField, validators
from sqlalchemy import select
from passlib.context import CryptContext

from ..db import User, db_manager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    def validate_name(self, field):
        with db_manager.Session() as session:
            user = session.scalar(select(User).where(User.name == field.data))
            if user:
                raise ValidationError('Имя пользователя уже существует')

            return field.data


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

    def validate_password(self, field):
        with db_manager.Session() as session:
            user = session.scalar(select(User).where(User.name == self.name.data))
            if not user:
                raise ValidationError('Пользователя не существует')

            if not pwd_context.verify(field.data, user.password):
                raise ValidationError('Неверный пароль')

            return field.data
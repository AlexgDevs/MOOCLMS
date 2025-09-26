from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, NumberRange
from wtforms import IntegerField, PasswordField, SubmitField, StringField, TextAreaField, validators, IntegerRangeField
from sqlalchemy import select



class CreateModuleForm(FlaskForm):
    name = StringField(
        'Название модуля', 
        validators=[
            DataRequired('Обязательное поле')
        ],
        render_kw={"placeholder": "Введите название модуля"}
    )

    submit = SubmitField('Создать модуль курса')
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, NumberRange
from wtforms import IntegerField, PasswordField, SubmitField, StringField, TextAreaField, validators, IntegerRangeField
from sqlalchemy import select

# нужно кароче создать форму создания курсов
# модулей 
# уроков и всякой хуйни еще

class CreateFreeCourseForm(FlaskForm):
    name = StringField(
        'Название курса', 
        validators=[
            DataRequired('Обязательное поле')
        ],
        render_kw={"placeholder": "Введите название курса"}
    )

    description = TextAreaField(  
        'Описание курса', 
        validators=[
            DataRequired('Обязательное поле')
        ],
        render_kw={"placeholder": "Введите описание курса", "rows": 4}
    )

    submit = SubmitField('Создать бесплатный курс')


class CreatePremiumCourseForm(FlaskForm):
    name = StringField(
        'Название курса', 
        validators=[
            DataRequired('Обязательное поле')
        ],
        render_kw={"placeholder": "Введите название курса"}
    )

    description = TextAreaField(  
        'Описание курса', 
        validators=[
            DataRequired('Обязательное поле')
        ],
        render_kw={"placeholder": "Введите описание курса", "rows": 4}
    )

    price = IntegerField(  
        'Цена курса',
        validators=[
            DataRequired('Обязательное поле'),
            NumberRange(min=0, message='Цена не может быть отрицательной')
        ],
        render_kw={"placeholder": "Укажите цену в рублях"}
    )

    submit = SubmitField('Создать платный курс')
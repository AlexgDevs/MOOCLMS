from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms import IntegerField, SubmitField, StringField, TextAreaField


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

    category = StringField(
        'Категория', 
        validators=[
            Optional()
        ],
        render_kw={"placeholder": "Введите категорию курса. Например: IT"}
    )

    cover_url = StringField(
        'Обложка курса URL',
        validators=[
        Optional()
        ]
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

    category = StringField(
        'Категория', 
        validators=[
            Optional()
        ],
        render_kw={"placeholder": "Введите категорию курса. Например: IT"}
    )

    price = IntegerField(  
        'Цена курса',
        validators=[
            DataRequired('Обязательное поле'),
            NumberRange(min=0, message='Цена не может быть отрицательной')
        ],
        render_kw={"placeholder": "Укажите цену в рублях"}
    )


    cover_url = StringField(
        'Обложка курса URL',
        validators=[
        Optional()
        ]
    )


    submit = SubmitField('Создать платный курс')
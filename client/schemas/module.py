from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField


class CreateModuleForm(FlaskForm):
    name = StringField(
        'Название модуля', 
        validators=[
            DataRequired('Обязательное поле')
        ],
        render_kw={"placeholder": "Введите название модуля"}
    )

    submit = SubmitField('Создать модуль курса')
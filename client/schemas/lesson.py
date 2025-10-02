from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Optional
from wtforms import FileField, SelectField, SubmitField, StringField, TextAreaField


class CreateLessonForm(FlaskForm):
    name = StringField('Название урока', validators=[
        DataRequired(message='Название урока обязательно'),
        Length(min=2, max=255, message='Название должно быть от 2 до 255 символов')
    ])
    
    content = TextAreaField('Содержание урока', validators=[
        DataRequired(message='Содержание урока обязательно'),
        Length(min=10, max=8096, message='Содержание должно быть от 10 до 8096 символов')
    ])

    lesson_type = SelectField('Тип урока', choices=[
        ('text', 'Текстовый урок'),
        ('video', 'Видео урок'), 
        ('quiz', 'Тест/Квиз')
    ], validators=[DataRequired()])

    image = FileField('Изображение урока', validators=[
        Optional()
    ])

    submit = SubmitField('Создать урок')
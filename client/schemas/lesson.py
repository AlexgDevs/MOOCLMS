from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, NumberRange
from wtforms import IntegerField, PasswordField, SubmitField, StringField, TextAreaField, validators, IntegerRangeField
from sqlalchemy import select

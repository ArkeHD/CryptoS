from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, IntegerField, StringField, TextAreaField, SelectMultipleField


class BalanceForm(FlaskForm):
    balance = IntegerField("1 рубль = 10 Гео", validators=[DataRequired(), NumberRange(min=1, max=100000)], render_kw={'step': 1})
    submit = SubmitField('Конвертировать')
    back = SubmitField('Вернуться', render_kw={'formnovalidate': True})
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, IntegerField, StringField, TextAreaField, SelectMultipleField


class GamesForm(FlaskForm):
    name = StringField('Название игры', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField("Описание")
    price = IntegerField("Цена", validators=[DataRequired(), NumberRange(min=0, max=100000)], render_kw={'step': 1})
    genres = SelectMultipleField('Жанры',
        choices=[('1', 'Песочница'), ('2', 'Рогалик'),
                 ('3', 'Шутер'), ('4', 'Хоррор'),
                 ('5', 'Метроидвания'), ('6', 'Онлайн'),
                 ('7', 'Оффлайн'), ('8', 'Симулятор'),
                 ('9', 'Экшен'), ('10', 'Казуальные'),
                 ('11', 'Другое'),])
    photo = FileField(validators=[Optional()])
    submit = SubmitField('Сохранение')
    back = SubmitField('Вернуться', render_kw={'formnovalidate': True})
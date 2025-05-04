from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=20)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), Length(min=5, max=20)])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')

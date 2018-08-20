from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .validators import UniqueEmail, UniqueUsername


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    fullname = StringField(label='Fullname', validators=[DataRequired(), Length(min=5, max=64)])
    email = StringField(label='Email', validators=[DataRequired(), Email(), UniqueEmail()])
    username = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=64), UniqueUsername()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label='Comfirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ProfileForm(RegisterForm):
    roles = SelectMultipleField(label='Roles')
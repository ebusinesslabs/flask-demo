from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    fullname = StringField(label='Fullname', validators=[DataRequired(), Length(min=5, max=64)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    username = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label='Comfirm Password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Sign On')

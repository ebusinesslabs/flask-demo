from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .validators import UniqueEmail, UniqueUsername
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(label=_l('Username'), validators=[DataRequired()])
    password = PasswordField(label=_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(label=_l('Remember me'))
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    fullname = StringField(label=_l('Fullname'), validators=[DataRequired(), Length(min=5, max=64)])
    email = StringField(label=_l('Email'), validators=[DataRequired(), Email(), UniqueEmail()])
    username = StringField(label=_l('Username'), validators=[DataRequired(), Length(min=4, max=64), UniqueUsername()])
    password = PasswordField(label=_l('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label=_l('Comfirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))


class ProfileForm(RegisterForm):
    roles = SelectMultipleField(label=_l('Roles'))


class ForgotPasswordForm(FlaskForm):
    email = StringField(label=_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Reset Password'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label=_l('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label=_l('Comfirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset Password'))
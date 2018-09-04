from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from ..auth.validators import UniqueEmail, UniqueUsername
from ..auth.models import Role


class UpdateForm(FlaskForm):
    id = HiddenField(label='ID')
    fullname = StringField(label='Full Name', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired(), UniqueUsername()])
    email = StringField(label='Email', validators=[DataRequired(), Email(), UniqueEmail()])
    password = PasswordField(label='Password', validators=[Length(min=8)])
    confirm_password = PasswordField(label='Comfirm Password', validators=[EqualTo('password')])
    roles = SelectMultipleField('Roles')
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, **kwargs)
        self.roles.choices = [(role.name, role.name) for role in Role.query.all()]

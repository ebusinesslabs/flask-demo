from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from .validators import UniqueUsername, UniqueEmail
from ..auth.models import Role


class UpdateForm(FlaskForm):
    id = HiddenField(label='ID')
    fullname = StringField(label='Full Name', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired(), UniqueUsername()])
    email = StringField(label='Email', validators=[DataRequired(), Email(), UniqueEmail()])
    password = PasswordField(label='Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField(label='Comfirm Password', validators=[EqualTo('password')])
    status = BooleanField(label='Status')
    roles = QuerySelectMultipleField('Roles')
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, **kwargs)
        self.roles.query = Role.query.all()

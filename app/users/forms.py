from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from .validators import UniqueUsername, UniqueEmail
from ..auth.models import Role
from flask_babel import lazy_gettext as _l

class ProfileForm(FlaskForm):
    id                  = HiddenField(label='ID')
    fullname            = StringField(label=_l('Full name'), validators=[DataRequired()])
    username            = StringField(label=_l('Username'), validators=[DataRequired(), UniqueUsername()])
    email               = StringField(label=_l('Email'), validators=[DataRequired(), Email(), UniqueEmail()])
    password            = PasswordField(label=_l('Password'), validators=[Optional(), Length(min=8)])
    confirm_password    = PasswordField(label=_l('Comfirm Password'), validators=[EqualTo('password')])
    status              = BooleanField(label=_l('Status'))
    roles               = QuerySelectMultipleField('Roles')
    submit              = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, **kwargs)
        self.roles.query = Role.query.all()


class AddUserForm(ProfileForm):
    password =  PasswordField(label=_l('Password'), validators=[Length(min=8)])
    submit =    SubmitField('Add')
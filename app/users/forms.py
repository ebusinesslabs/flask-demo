from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from ..auth.validators import UniqueEmail


class UpdateForm(FlaskForm):
    fullname = StringField(label='Full Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(), UniqueEmail])
    submit = SubmitField('Update')

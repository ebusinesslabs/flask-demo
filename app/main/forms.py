from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from flask_babel import lazy_gettext as _l


class SettingsForm(FlaskForm):
    offline = BooleanField(label=_l('Offline'))
    registration = BooleanField(label=_l('Registration'))
    submit = SubmitField(label=_l('Save'))
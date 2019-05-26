from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, TextAreaField, HiddenField, DateTimeField
from wtforms.validators import Length
from flask_wtf.file import FileAllowed
from flask_babel import lazy_gettext as _l


class AddForm(FlaskForm):
    title = StringField(label=_l('Title'), validators=[Length(min=4, max=128)])
    slug = StringField(label=_l('Slug'), validators=[Length(min=3, max=256)])
    body = TextAreaField(label=_l('Body'))
    status = BooleanField(label=_l('Status'))
    image = FileField(label=_l('Image'), validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'jpg or png')])
    submit = SubmitField(label=_l('Submit'))


class UpdateForm(AddForm):
    id = HiddenField(label='id')
    createdat = DateTimeField(label=_l('Created at'))
    del_image = BooleanField(label=_l('Delete'))
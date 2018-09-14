from ..auth.models import User
from wtforms.validators import *


class UniqueEmail(object):
    """
    Checks if the email value is unique
    """
    def __call__(self, form, field):
        u = User.query.filter(User.email == field.data, User.id != form.id.data).first()
        if u is not None:
            raise ValidationError('Email must be unique')


class UniqueUsername(object):
    """
    Checks if the username value is unique
    """
    def __call__(self, form, field):
        u = User.query.filter(User.username == field.data, User.id != form.id.data).first()
        if u is not None:
            raise ValidationError('Username must be unique')

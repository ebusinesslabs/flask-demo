from .models import User
from wtforms.validators import *


class UniqueEmail(object):
    """
    Checks if the email value is unique
    """
    def __call__(self, form, field):
        u = User.query.filter_by(email=field.data).first()
        if u is not None:
            raise ValidationError('Email must be unique')


class UniqueUsername(object):
    """
    Checks if the username value is unique
    """
    def __call__(self, form, field):
        u = User.query.filter_by(username=field.data).first()
        if u is not None:
            raise ValidationError('Username must be unique')

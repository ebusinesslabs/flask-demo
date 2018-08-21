from functools import wraps
from flask import redirect, flash, url_for
from flask_login import current_user


def role_required(*allowed_roles):
    """
    Does the user have permissions to view the page?
    :param allowed_roles: one or more allowed roles
    :return: Function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for role in current_user.roles:
                if role.name in allowed_roles:
                    return f(*args, **kwargs)

            flash('You do not have permission to view this resource', category='danger')
            return redirect(url_for('main.index'))

        return decorated_function

    return decorator

from flask import render_template, url_for, flash, request
from . import bp
from flask_login import login_required
from ..auth.decorators import role_required
from ..auth.models import User
from .forms import UpdateForm


@bp.route('/users')
@login_required
@role_required('Administrator')
def list_users():
    users = User.query.order_by(User.id).all()
    return render_template('users/list.html', users=users)


@bp.route('/user/<id>', methods=['GET', 'POST'])
def user_update(id):
    user = User.query.get(id)
    form = UpdateForm(obj=user)
    return render_template('users/update.html', form=form)

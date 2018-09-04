from flask import render_template, url_for, flash, redirect
from . import bp
from flask_login import login_required
from ..auth.decorators import role_required
from ..auth.models import User, Role
from .forms import UpdateForm


@bp.route('/users')
@login_required
@role_required('Administrator')
def list_users():
    users = User.query.order_by(User.id).all()
    return render_template('users/list.html', users=users)


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
def user_update(id):
    user = User.query.get(id)  # type: User
    form = UpdateForm(obj=user)
    if form.validate_on_submit():
        user.fullname = form.fullname.data
        user.username = form.username.data
        if form.password.data is None:
            user.set_password(form.password.data)
        user.email = form.email.data
        user.status = True
        role = Role(name='User')
        user.roles = [role]
        user.save()
        flash('User saved successfully.', category='success')
        return redirect(url_for('list_users'))
    return render_template('users/update.html', form=form)

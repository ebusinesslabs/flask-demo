from flask import render_template, url_for, flash, redirect, request, current_app
from . import bp
from flask_login import login_required
from ..auth.decorators import role_required
from ..auth.models import User, Role
from .forms import ProfileForm, AddUserForm
from flask_babel import _
import os
import uuid


@bp.route('/users')
@login_required
@role_required('Administrator')
def list():
    query_user = User.query
    if request.args:
        for parameter in request.args.items():
            if parameter[0] == 'email':
                query_user = query_user.filter(User.email.like('%' + parameter[1] + '%'))
            elif parameter[0] == 'role':
                query_user = query_user.join('roles').filter(Role.id == parameter[1])
    page = request.args.get('page', 1, type=int)
    users = query_user.order_by(User.id).paginate(page, 10, False)
    return render_template('users/list.html', users=users)


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrator')
def update(id):
    user = User.query.get(id)  # type: User
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        user.fullname = form.fullname.data
        user.username = form.username.data
        if form.password.data:
            user.set_password(form.password.data)
        user.email = form.email.data
        user.status = form.status.data
        user.roles = form.roles.data
        if form.delete.data:
            delete_image(user.image)
            user.image = None
        if form.image.data:
            delete_image(user.image)
            user.image = upload_image(form.image.data)
        user.save()
        flash(_('User saved successfully.'), category='success')
        return redirect(url_for('users.list'))
    return render_template('users/update.html', form=form)


@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
@role_required('Administrator')
def add():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User()
        user.fullname = form.fullname.data
        user.username = form.username.data
        user.set_password(form.password.data)
        user.email = form.email.data
        user.status = form.status.data
        user.roles = form.roles.data
        user.image = upload_image(form.image.data)
        user.save()
        flash(_('User saved successfully.'), category='success')
        return redirect(url_for('users.list'))

    return render_template('users/add.html', form=form)


def upload_image(imagedata):
    if imagedata:
        extension = os.path.splitext(imagedata.filename)[1]
        unique_filename = uuid.uuid4().hex + extension
        imagedata.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
        return unique_filename
    return None


def delete_image(image):
    if image and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], image)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image))
        return True
    return False

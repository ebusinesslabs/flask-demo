from ..auth import bp
from flask import render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from .models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User()
        user.fullname = register_form.fullname.data
        user.username = register_form.username.data
        user.set_password(register_form.password.data)
        user.email = register_form.email.data
        user.status = True
        user.save()
        flash('You are now a registered user.', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = register_form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
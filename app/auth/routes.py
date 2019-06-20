from ..auth import bp
from flask import render_template, redirect, url_for, flash, request, current_app
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user
from .models import User, Role
from ..main.models import Config
import hashlib, time
from flask_mail import Mail, Message
from distutils import util

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            user = User.query.filter_by(email=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password.')
                return redirect(url_for('auth.login'))
        if not user.status:
            flash('Your account has beeen disabled.')
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
    registration = Config.query.filter(Config.entity == 'registration').first()
    if register_form.validate_on_submit():
        user = User()
        user.fullname = register_form.fullname.data
        user.username = register_form.username.data
        user.set_password(register_form.password.data)
        user.email = register_form.email.data
        user.status = True
        role = Role.query.filter_by(name='User').first()
        user.roles = [role]
        user.save()
        flash('You are now a registered user.', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=register_form, registration=util.strtobool(registration.value))


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    forgot_form = ForgotPasswordForm()
    if forgot_form.validate_on_submit():
        user = User.query.filter_by(email=forgot_form.email.data).first()
        if user is None:
            flash('No such email address in our database.', category='danger')
            return redirect(url_for('auth.forgot'))
        md5 = hashlib.new('md5', (time.asctime() + user.email).encode('utf-8'))
        user.token = md5.hexdigest()
        user.save()
        mail = Mail(current_app)
        message = Message('[Flask Demo] - Reset password', sender='dvossos@example.com', recipients=[user.email])
        # message.body = 'Please follow link to reset password.\n' \
        #                + request.host_url \
        #                + 'reset' \
        #                + '?email=' + user.email \
        #                + '&token=' + md5.hexdigest()
        message.body = 'Please follow the link to reset your password\n' \
                       + url_for('auth.reset', _external=True, email=user.email, token=md5.hexdigest())
        try:
            mail.send(message)
            flash('Check your email', category='success')
        except Exception as exception:
            flash('Unable to send mail, ' + exception.args[1], category='danger')
    return render_template('auth/forgot.html', form=forgot_form)


@bp.route('/reset', methods=['GET', 'POST'])
def reset():
    reset_form = ResetPasswordForm()
    email = request.args.get('email')
    token = request.args.get('token')
    if reset_form.validate_on_submit():
        user = User.query.filter_by(email=email, token=token).first()
        if user is None:
            flash('User has never asked for password reset', category='danger')
            return redirect(url_for('.reset'))
        user.token = None
        user.set_password(reset_form.password.data)
        user.save()
        flash('Password has been changed.', category='success')
    return render_template('auth/reset.html', form=reset_form)

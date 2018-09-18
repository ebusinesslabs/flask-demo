from ..main import bp
from flask import render_template
from flask_login import login_required
from ..auth.decorators import role_required
from ..auth.models import User
from sqlalchemy import func


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/dashboard')
@login_required
@role_required('Administrator')
def dashboard():
    records = User.query.with_entities(User.created, func.count()).group_by(func.date(User.created)).all()
    users = []
    dates = []
    for record in records:
        users.append(record[1])
        dates.append(record[0].strftime('%d/%m/%Y'))
    data = {'users_count': User.query.count(), 'users': users, 'dates': dates}
    return render_template('main/dashboard.html', data=data)

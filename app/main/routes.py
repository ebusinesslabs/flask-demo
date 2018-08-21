from ..main import bp
from flask import render_template
from flask_login import login_required
from ..auth.decorators import role_required

@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/dashboard')
@login_required
@role_required('Administrator')
def dashboard():
    return render_template('main/dashboard.html')
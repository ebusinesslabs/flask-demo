from ..main import bp
from flask import render_template
from flask_login import login_required


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')
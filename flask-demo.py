from app import create_app, db
from app.auth.models import User, Role
from flask import render_template
app = create_app()


@app.errorhandler(403)
def forbidden(error):
    """
    Error handler for permission denied

    :param error: werkzeug.exceptions.Forbidden
    :return: renders a template
    """
    return render_template('errors/error.html', error=error), 403


@app.errorhandler(500)
def internal_error(error):
    """
    Error handler for internal server error
    :param error: werkzeug.exceptions.Forbidden
    :return: renders a template
    """
    return render_template('errors/error.html', error=error), 500


@app.errorhandler(404)
def not_found(error):
    """
    Error hanlder for page not found

    :param error: werkzeug.exceptions.Forbidden
    :return: renders a template
    """
    return render_template('errors/error.html', error=error), 404


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}

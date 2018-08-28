from ..errors import bp
from flask import render_template, current_app


@bp.app_errorhandler(403)
def forbidden(error):
    """
    Error handler for permission denied

    :param error: werkzeug.exceptions.Forbidden
    :return: renders a template
    """
    return render_template('errors/error.html', error=error), 403


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Error handler for internal server error
    :param error: werkzeug.exceptions.Forbidden
    :return: renders a template
    """
    return render_template('errors/error.html', error=error), 500


@bp.app_errorhandler(404)
def not_found(error):
    """
    Error hanlder for page not found

    :param error: werkzeug.exceptions.Forbidden
    :return: renders a template
    """
    return render_template('errors/error.html', error=error), 404

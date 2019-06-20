from app import create_app, db
from app.auth.models import User, Role
from app.articles.models import Article
from app.main.models import Config
from flask import g, abort, request
import pytz, flask
from distutils import util

app = create_app()


@app.url_defaults
def set_language_code(endpoint, values):
    # runs for every url_for() and injects values
    if 'lang_code' in values or not g.get('lang_code', None):
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    # The url_value_preprocessor() registers the get_lang_code() function, which obtains and sets the language code
    # from the request on the application globals flask.g object.
    if values is not None:
        g.lang_code = values.pop('lang_code', None)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Article': Article, 'Config': Config}


@app.template_filter('localdatetime')
def localdatetime(value):
    tz = pytz.timezone('Europe/Athens')  # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime('%d/%m/%Y %H:%M:%S')


@app.template_global()
def flask_version():
    return flask.__version__


@app.before_request
def set_offline():
    offline = Config.query.filter(Config.entity == 'offline').first()
    endpoints = ['main.settings', 'auth.login', 'auth.logout']
    if util.strtobool(offline.value) and request.endpoint not in endpoints:
        abort(503)

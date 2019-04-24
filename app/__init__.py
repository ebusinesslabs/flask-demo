from flask import Flask, request, current_app, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_babel import Babel


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
migrate = Migrate()
babel = Babel()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)

    from .errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    app.register_blueprint(errors_bp, url_prefix='/<lang_code>')

    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(main_bp, url_prefix='/<lang_code>')

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth_bp, url_prefix='/<lang_code>')

    from .users import bp as users_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(users_bp, url_prefix='/<lang_code>')

    # logger file handler when DEBUG = False
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask-demo.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)

    return app

@babel.localeselector
def get_locale():
    return g.get('lang_code', current_app.config['BABEL_DEFAULT_LOCALE'])
    #return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from flask import render_template, request, abort, flash
from flask_login import login_required
from sqlalchemy import func

from ..articles.models import Article
from ..auth.models import User
from ..auth.decorators import role_required
from ..main import bp
from .forms import SettingsForm
from .models import Config
import sys, platform
from distutils import util


@bp.route('/')
def index():
    articles = Article.query.filter_by(status=1).order_by(Article.createdat.desc()).all()
    return render_template('main/index.html', articles=articles)


@bp.route('/view/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.status:
        return render_template('main/article_view.html', article=article)
    abort(404)


@bp.route('/blank')
def blank():
    return render_template('main/blank.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    # MySQL query
    # records = User.query.with_entities(func.date(User.created), func.count())\
    #     .group_by(func.date(User.created))\
    #     .all()

    list_articles_per_user = Article.query.join(User).with_entities(User.username, func.count()) \
        .group_by(Article.user_id) \
        .all()
    # convert [(u'dvossos', 7), (u'user1', 1), (u'user3', 2), (u'user4', 1), (u'editor1', 1)]
    # to [(u'dvossos', u'user1', u'user3', u'user4', u'editor1'), (7, 1, 2, 1, 1)]
    articles_per_user = list(zip(*list_articles_per_user))

    articles_records = Article.query.with_entities(Article.createdat, func.count()) \
        .group_by(func.date(Article.createdat)) \
        .all()
    articles = []
    articles_dates = []
    for record in articles_records:
        articles.append(record[1])
        articles_dates.append(record[0].strftime('%d/%m/%Y'))
    inactive_articles = Article.query.filter(Article.status == False).all()
    data = {
        'users_count': User.query.count(),
        'articles_count': Article.query.count(),
        'articles': articles,
        'articles_dates': articles_dates,
        'articles_per_user': articles_per_user,
        'inactive_articles': inactive_articles,
    }
    return render_template('main/dashboard.html', data=data)


@bp.route('/search', methods=['POST'])
def search_list():
    articles = Article.query\
        .filter(Article.body.like('%' + request.form['search'] + '%'))\
        .filter(Article.status == 1)\
        .all()
    return render_template('main/search_list.html', articles=articles)


@bp.route('/sysinfo', methods=['GET'])
@login_required
@role_required('Administrator')
def sysinfo():
    data = {'python_version': sys.version, 'platform_version': platform.version()}
    return render_template('main/sysinfo.html', data=data)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
@role_required('Administrator')
def settings():
    offline = Config.query.filter(Config.entity == 'offline').first()
    if offline is None:
        offline = Config(entity='offline', value='False')
    registration = Config.query.filter(Config.entity == 'registration').first()
    if registration is None:
        registration = Config(entity='registration', value='False')
    form = SettingsForm(
        offline = util.strtobool(offline.value),
        registration = util.strtobool(registration.value)
    )
    if form.is_submitted():
        offline.value = str(form.offline.data)
        registration.value = str(form.registration.data)
        offline.save()
        registration.save()
        flash('Global settings saved successfully.')
    return render_template('main/global_settings.html', form=form)

from ..main import bp
from flask import render_template
from flask_login import login_required
from ..auth.decorators import role_required
from ..auth.models import User
from ..articles.models import Article
from sqlalchemy import func


@bp.route('/')
def index():
    articles = Article.query.filter_by(status=1).all()
    return render_template('main/index.html', articles=articles)


@bp.route('/view/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('main/article_view.html', article=article)


@bp.route('/blank')
def blank():
    return render_template('main/blank.html')


@bp.route('/dashboard')
@login_required
@role_required('Administrator')
def dashboard():
    # MySQL query
    # records = User.query.with_entities(func.date(User.created), func.count())\
    #     .group_by(func.date(User.created))\
    #     .all()

    # SQLite query
    records = User.query.with_entities(User.created, func.count()) \
        .group_by(func.date(User.created)) \
        .all()

    users = []
    dates = []
    for record in records:
        users.append(record[1])
        dates.append(record[0].strftime('%d/%m/%Y'))
    data = {'users_count': User.query.count(), 'users': users, 'dates': dates, 'articles_count': Article.query.count()}
    return render_template('main/dashboard.html', data=data)

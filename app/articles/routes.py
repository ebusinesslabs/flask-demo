from .models import Article
from .forms import AddForm
from flask_login import current_user, login_required
from ..auth.decorators import role_required
from . import bp
from flask import render_template, request, flash, redirect, url_for, abort
from flask_babel import _


@bp.route('/articles')
@login_required
@role_required('Administrator', 'Editor', 'User')
def list():
    page = request.args.get('page', 1, type=int)
    if current_user.has_role('Administrator') or current_user.has_role('Editor'):
        articles = Article.query.order_by(Article.createat).paginate(page, 10, False)
    else:
        articles = Article.query.filter_by(createdby=current_user.id).paginate(page, 10, False)
    return render_template('articles/list.html', articles=articles)


@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
@role_required('Administrator', 'Editor', 'User')
def add():
    form = AddForm()
    if form.validate_on_submit():
        article = Article()
        article.title = form.title.data
        article.slug = form.slug.data
        article.body = form.body.data
        article.status = form.status.data
        article.createdby = current_user.id
        article.save()
        flash(_('Article saved successfully.'), category='success')
        return redirect(url_for('articles.list'))
    return render_template('articles/add.html', form=form)


@bp.route('/article/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrator', 'Editor', 'User')
def update(id):
    article = Article.query.get(id)
    if not (current_user.has_role('Administrator') or current_user.has_role('Editor')) and current_user.id != article.createdby:
        abort(403)
    return 'Article title: {}'.format(article.title)

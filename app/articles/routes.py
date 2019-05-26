from .models import Article
from .forms import AddForm, UpdateForm
from flask_login import current_user, login_required
from ..auth.decorators import role_required
from . import bp
from flask import render_template, request, flash, redirect, url_for, abort, current_app
from flask_babel import _
import os, uuid

@bp.route('/articles')
@login_required
@role_required('Administrator', 'Editor', 'User')
def list():
    page = request.args.get('page', 1, type=int)
    if current_user.has_role('Administrator') or current_user.has_role('Editor'):
        articles = Article.query.order_by(Article.createdat).paginate(page, 10, False)
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
        article.image = upload_image(form.image.data)
        article.save()
        flash(_('Article saved successfully.'), category='success')
        return redirect(url_for('articles.list'))
    return render_template('articles/add.html', form=form)


@bp.route('/article/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrator', 'Editor', 'User')
def update(id):
    article = Article.query.get(id)
    form = UpdateForm(obj=article)
    if not (current_user.has_role('Administrator') or current_user.has_role('Editor')) and current_user.id != article.createdby:
        abort(403)
    if form.validate_on_submit():
        article.title = form.title.data
        article.slug = form.slug.data
        article.body = form.body.data
        article.status = form.status.data
        if form.del_image.data:
            delete_image(article.image)
            article.image = None
        if form.image.data:
            delete_image(article.image)
            article.image = upload_image(form.image.data)
        article.save()
        flash(_('Article saved successfully.'), category='success')
        return redirect(url_for('articles.list'))
    return render_template('articles/update.html', form=form)


def upload_image(imagedata):
    if imagedata:
        extension = os.path.splitext(imagedata.filename)[1]
        unique_filename = uuid.uuid4().hex + extension
        imagedata.save(os.path.join(current_app.config['ARTICLES_UPLOAD_FOLDER'], unique_filename))
        return unique_filename
    return None

def delete_image(image):
    if image and os.path.exists(os.path.join(current_app.config['ARTICLES_UPLOAD_FOLDER'], image)):
        os.remove(os.path.join(current_app.config['ARTICLES_UPLOAD_FOLDER'], image))
        return True
    return False

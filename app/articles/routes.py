from .models import Article
from .forms import AddForm, UpdateForm, SearchForm
from flask_login import current_user, login_required
from ..auth.decorators import role_required
from . import bp
from flask import render_template, request, flash, redirect, url_for, abort, current_app
from flask_babel import _
import os, uuid, re
from ..auth.models import User


@bp.route('/articles')
@login_required
@role_required('Administrator', 'Editor', 'User')
def list_view():
    # define search form and populate previous search criteria
    form = SearchForm(data=request.args.items())
    # because 'author' QuerySelectField has been populated with objects of type <User>
    # it won't be selected just with the id from query string (previous search criteria)
    # We get object User from id
    if request.args.get('author'):
        author = User.query.get(request.args.get('author'))
        form.author.data = author

    query_article = Article.query
    if request.args:
        for parameter in request.args.items():
            if parameter[0] == 'title' and parameter[1]:
                query_article = query_article.filter(Article.title.like('%' + parameter[1] + '%'))
            elif parameter[0] == 'author' and parameter[1] != '__None':
                query_article = query_article.join('author').filter(User.id == parameter[1])
            elif parameter[0] == 'status' and parameter[1] != '':
                query_article = query_article.filter(Article.status == parameter[1])
    page = request.args.get('page', 1, type=int)
    if current_user.has_role('Administrator') or current_user.has_role('Editor'):
        articles = query_article.order_by(Article.createdat).paginate(page, 10, False)
    else:
        articles = query_article.filter_by(user_id=current_user.id).paginate(page, 10, False)
    # pass search filter in pagination
    query_string = re.sub('page=\d*&*', '', request.query_string.decode('utf-8'))
    return render_template('articles/list.html', articles=articles, form=form, query_string=query_string)


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
        article.user_id = current_user.id
        article.image = upload_image(form.image.data)
        article.save()
        flash(_('Article saved successfully.'), category='success')
        return redirect(url_for('articles.list_view'))
    return render_template('articles/add.html', form=form)


@bp.route('/article/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Administrator', 'Editor', 'User')
def update(id):
    article = Article.query.get(id)
    form = UpdateForm(obj=article)
    if not (current_user.has_role('Administrator') or current_user.has_role(
            'Editor')) and current_user.id != article.user_id:
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
        return redirect(url_for('articles.list_view'))
    return render_template('articles/update.html', form=form)


def upload_image(imagedata):
    if imagedata:
        extension = os.path.splitext(imagedata.filename)[1]
        unique_filename = uuid.uuid4().hex + extension
        imagedata.save(os.path.join(current_app.config['ARTICLES_UPLOAD_FOLDER'], unique_filename))
        return unique_filename
    return None


@bp.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
@role_required('Administrator', 'Editor', 'User')
def delete(article_id):
    article = Article.query.get_or_404(article_id)
    if not (current_user.has_role('Administrator') or current_user.has_role(
            'Editor')) and current_user.id != article.createdby:
        abort(403)
    article.delete()
    delete_image(article.image)
    return redirect(url_for('articles.list_view'))


def delete_image(image):
    if image and os.path.exists(os.path.join(current_app.config['ARTICLES_UPLOAD_FOLDER'], image)):
        os.remove(os.path.join(current_app.config['ARTICLES_UPLOAD_FOLDER'], image))
        return True
    return False

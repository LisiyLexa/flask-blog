from flask import Blueprint, render_template, redirect, request, abort
from app.db_session import create_session
from flask_login import current_user, login_required
from app.models import News
from .forms import NewsForm
from app.utils import random_code

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    db_sess = create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True)
        )
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("blog/index.html", news=news)


@blog_bp.route("/post/<news_code>", methods=["GET", "POST"])
@login_required
def edit_post(news_code):
    form = NewsForm()
    if request.method == "GET":
        db_sess = create_session()
        news = (
            db_sess.query(News)
            .filter(News.news_code == news_code, News.user == current_user)
            .first()
        )
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        news = (
            db_sess.query(News)
            .filter(News.news_code == news_code, News.user == current_user)
            .first()
        )
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("blog/create_news.html", title="Editing news", form=form)


@blog_bp.route("/create-news", methods=["GET", "POST"])
@login_required
def add_post():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        while True:
            code = random_code()
            if not db_sess.query(News).filter_by(news_code=code).first():
                break
        news.news_code = code
        current_user.news.append(news)

        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("/")
    return render_template("blog/create_news.html", title="Creating news", form=form)


@blog_bp.route("/post-delete/<news_code>", methods=["GET", "POST"])
@login_required
def delete_post(news_code):
    db_sess = create_session()
    news = (
        db_sess.query(News)
        .filter(News.news_code == news_code, News.user == current_user)
        .first()
    )
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")

from flask import Blueprint, render_template, redirect
from flask_login import login_required, login_user, logout_user
from .forms import LoginForm, RegisterForm
import app.db_session as db_session
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "auth/login.html", message="Wrong login or password", form=form
        )
    return render_template("auth/login.html", title="Авторизация", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Registration",
                form=form,
                message="Passwords not matching.",
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Registration",
                form=form,
                message="User already exists.",
            )
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("login")
    return render_template("auth/register.html", title="Registration", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

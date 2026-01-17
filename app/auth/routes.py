from flask import Blueprint, render_template, redirect
from .forms import LoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/success")
    return render_template("auth/login.html", title="Login Page", form=form)


@auth_bp.route("/register")
def register():
    return "Register Page"

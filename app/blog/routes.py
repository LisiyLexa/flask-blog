from flask import Blueprint

blog_bp = Blueprint('blog', __name__)

@blog_bp.route("/")
def index():
    return "Blog Homepage"

@blog_bp.route("/post/<int:id>")
def post(id):
    return f"Post {id}"

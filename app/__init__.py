from flask import Flask
from flask_login import LoginManager
from .db_session import global_init, create_session
from .models import User


def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = create_session()
        return db_sess.query(User).get(user_id)

    # Config (for now, very simple)
    app.config["SECRET_KEY"] = "dev"  # TODO: load from env later

    # Import blueprints
    from .auth.routes import auth_bp
    from .blog.routes import blog_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    global_init("main.db")

    return app

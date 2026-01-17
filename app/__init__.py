from flask import Flask
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    # Config (for now, very simple)
    app.config["SECRET_KEY"] = "dev"  # TODO: load from env later

    # Import blueprints
    from .auth.routes import auth_bp
    from .blog.routes import blog_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    return app

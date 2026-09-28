"""flask-blog: a simple JWT-authenticated blog API built with Flask and MongoDB."""

from flask import Flask
from flask_jwt_extended import JWTManager

from flask_blog.config import Config
from flask_blog.routes.auth import auth_bp
from flask_blog.routes.blogs import blog_bp

jwt = JWTManager()


def create_app(config_overrides: dict | None = None) -> Flask:
    """Application factory for the flask-blog API."""
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    return app


app = create_app()


def main():
    """Entry point for the ``flask-blog`` console script."""
    app.run(debug=True)


if __name__ == "__main__":
    main()

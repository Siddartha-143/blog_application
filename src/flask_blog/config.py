"""Application configuration loaded from environment variables."""

import os


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


class Config:
    """Central configuration for the flask-blog application.

    All sensitive values fall back to development defaults; set the
    corresponding environment variables in production.
    """

    MONGO_URI: str = _env(
        "MONGO_URI",
        "mongodb+srv://nexturn_db:1234567890@cluster0.8e7hoxk.mongodb.net/?appName=Cluster0",
    )
    JWT_SECRET_KEY: str = _env("JWT_SECRET_KEY", "my-secret-key")

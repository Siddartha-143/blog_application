"""Data-access helpers for the users collection."""

from typing import Optional

from flask_blog.db import user_collection


def find_user_by_email(email: str) -> Optional[dict]:
    """Return the user document with the given email, or None."""
    return user_collection.find_one({"email": email})


def create_user(name: str, email: str, hashed_password: str, user_id: str) -> None:
    """Insert a new user document."""
    user_collection.insert_one(
        {
            "name": name,
            "email": email,
            "hashed_password": hashed_password,
            "id": user_id,
        }
    )

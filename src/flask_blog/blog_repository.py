"""Data-access helpers for the blogs collection."""

from datetime import datetime
from typing import Optional

from flask_blog.db import blog_collection


def find_blog_by_id(blog_id: str) -> Optional[dict]:
    """Return the blog document with the given blog_id, or None."""
    return blog_collection.find_one({"blog_id": blog_id})


def create_blog(title: str, content: str, author_id: str, blog_id: str) -> None:
    """Insert a new blog document in draft status."""
    now = datetime.now()
    blog_collection.insert_one(
        {
            "title": title,
            "content": content,
            "author_id": author_id,
            "blog_id": blog_id,
            "status": "draft",
            "created_at": now,
            "updated_at": "not updated yet",
            "published_at": "not published yet",
        }
    )


def publish_blog(blog_id: str) -> None:
    """Mark an existing blog as published."""
    blog_collection.update_one(
        {"blog_id": blog_id},
        {"$set": {"status": "published", "published_at": datetime.now()}},
    )


def list_published_blogs() -> list[dict]:
    """Return all published blogs, oldest first, without Mongo internals."""
    blogs = list(blog_collection.find({"status": "published"}))
    blogs.sort(key=lambda blog: blog["published_at"])
    for blog in blogs:
        blog.pop("_id", None)
    return blogs

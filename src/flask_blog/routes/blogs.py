"""Blog routes: create, publish, and read blog posts."""

from uuid import uuid4

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from flask_blog.blog_repository import (
    create_blog,
    find_blog_by_id,
    list_published_blogs,
    publish_blog,
)
from flask_blog.repositories import find_user_by_email

blog_bp = Blueprint("blog", __name__)


def _current_user_id() -> str | None:
    """Return the id of the user attached to the current JWT, or None."""
    user = find_user_by_email(get_jwt_identity())
    return user["id"] if user else None


@blog_bp.post("/blog")
@jwt_required()
def add_blog():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return {"message": "Please enter some text for title or content"}, 400

    author_id = _current_user_id()
    if author_id is None:
        return {"message": "User not found"}, 401

    create_blog(
        title=title,
        content=content,
        author_id=author_id,
        blog_id=str(uuid4()),
    )
    return {"message": "Blog added successfully"}, 201


@blog_bp.put("/blogs/publish/<blog_id>")
@jwt_required()
def publish(blog_id):
    blog = find_blog_by_id(blog_id)
    if blog is None:
        return {"message": "Blog not found"}, 404

    if _current_user_id() != blog["author_id"]:
        return {"message": "Only the authors can publish their blogs"}, 400

    publish_blog(blog_id)
    return {"message": "Blog published successfully"}, 200


@blog_bp.get("/blogs/<blog_id>")
@jwt_required()
def get_blog(blog_id):
    blog = find_blog_by_id(blog_id)
    if blog is None:
        return {"message": f"No blog with this {blog_id} id"}, 404

    if blog["status"] != "published":
        return {"message": "This blog is not published yet"}, 400

    blog.pop("_id", None)
    return blog, 200


@blog_bp.get("/blogs")
@jwt_required()
def get_blogs():
    blogs = list_published_blogs()
    if not blogs:
        return {"message": "No blogs are published yet"}, 404
    return blogs, 200

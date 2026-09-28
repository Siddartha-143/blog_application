"""MongoDB client and collection accessors."""

from pymongo import MongoClient

from flask_blog.config import Config

mongo_client = MongoClient(Config.MONGO_URI)

_users_db = mongo_client["users"]
_blogs_db = mongo_client["blogs"]

user_collection = _users_db["users_collection"]
blog_collection = _blogs_db["blog_collection"]

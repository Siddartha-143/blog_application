from pymongo import MongoClient
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from uuid import uuid4
from datetime import datetime


url = "mongodb+srv://nexturn_db:1234567890@cluster0.8e7hoxk.mongodb.net/?appName=Cluster0"
mongo_client = MongoClient(url)
user_db = mongo_client["users"]
user_collection = user_db["users_collection"]
blog_db = mongo_client["blogs"]
blog_collection = blog_db["blog_collection"]

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "my-secret-key"
jwt = JWTManager(app)

@app.post("/user")
def add_user():
    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]
    old_user = user_collection.find_one({"email": email})

    if old_user:
        return {
            "message": "Please enter a different mail ID"
        }, 400

    password = generate_password_hash(password)
    user_id = str(uuid4())

    user_data = {
        "name": name,
        "email": email,
        "hashed_password": password,
        "id": user_id
    }
    user_collection.insert_one(user_data)
    return {
        "message": "User is added successfully"
    }, 200
@app.post("/login")
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    user = user_collection.find_one({"email": email})
    if user is None:
        return {
            "message": "Signup required"
        }, 401
    if not check_password_hash(user["hashed_password"], password):
        return {
            "message": "Invalid password"
        }, 401
    token = create_access_token(identity=email)
    return {
        "message": "Logged in successfully",
        "token": token
    }, 200
@app.post("/blog")
@jwt_required()
def add_blog():
    data = request.json
    title = data["title"]
    content = data["content"]
    if not title or not content:
        return {
            "message": "Please enter some text for title or content"
        }, 400
    email = get_jwt_identity()
    user = user_collection.find_one({"email": email})
    user_id = user["id"]
    blog_data = {
        "title": title,
        "content": content,
        "author_id": user_id,
        "blog_id": str(uuid4()),
        "status": "draft",
        "created_at": datetime.now(),
        "updated_at": "not updated yet",
        "published_at": "not published yet"
    }
    blog_collection.insert_one(blog_data)
    return {
        "message": "Blog added successfully"
    }, 201
@app.put("/blogs/publish/<blog_id>")
@jwt_required()
def publish(blog_id):
    blog = blog_collection.find_one({
        "blog_id": blog_id
    })
    if blog is None:
        return {
            "message": "Blog not found"
        }, 404
    email = get_jwt_identity()
    user = user_collection.find_one({
        "email": email
    })
    user_id = user["id"]
    if user_id != blog["author_id"]:
        return {
            "message": "Only the authors can publish their blogs"
        }, 400
    blog_collection.update_one(
        {"blog_id": blog_id},
        {
            "$set": {
                "status": "published",
                "published_at": datetime.now()
            }
        }
    )
    return {
        "message": "Blog published successfully"
    }, 200
@app.get("/blogs/<blog_id>")
@jwt_required()
def get_blog(blog_id):
    blog = blog_collection.find_one({
        "blog_id": blog_id
    })
    if blog is None:
        return {
            "message": f"No blog with this {blog_id} id"
        }, 400
    if blog["status"] != "published":
        return {
            "message": "This blog is not published yet"
        }, 400
    blog.pop("_id", None)
    return blog, 200
@app.get("/blogs")
@jwt_required()
def get_blogs():
    blogs = list(
        blog_collection.find({
            "status": "published"
        })
    )
    if not blogs:
        return {
            "message": "No blogs are published yet"
        }, 400
    blogs = sorted(
        blogs,
        key=lambda x: x["published_at"]
    )
    for blog in blogs:
        blog.pop("_id", None)
    return blogs, 200
if __name__ == "__main__":
    app.run(debug=True)
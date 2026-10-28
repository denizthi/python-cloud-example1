# app.py

# resource: https://blog.appsignal.com/2025/04/30/using-jwts-in-python-flask-rest-framework.html

import requests
from flask import Flask, request, jsonify
from database import SessionLocal
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models import PostsY, LikesY, CommentsY
from config import SERVER_C_URL
from interactions import like_post, comment_post, react_post, create_post

app = Flask(__name__)
load_dotenv()
app.config.from_pyfile("config.py")
jwt = JWTManager(app)


@app.route('/status')
def status():
    return 'I am Server Y'


@app.route("/new_user", methods=["POST"])
def new_user():
    credentials = request.get_json(silent=True) or {}
    email = credentials.get("email", "")
    password = credentials.get("password", "")
    n_user = {"email": email, "password": password}
    try:
        r = requests.post((str(SERVER_C_URL) + "/new_user"), json=n_user)
    except requests.RequestException:
        return jsonify(error="Cannot reach Server C")

    return r.json()

@app.route("/login", methods=["POST"])
def login():
    credentials = request.get_json(silent=True) or {}
    email = credentials.get("email", "")
    password = credentials.get("password", "")
    l_user = {"email": email, "password": password}
    try:
        r = requests.post((str(SERVER_C_URL) + "/login"), json=l_user)
    except requests.RequestException:
        return jsonify(error="Cannot reach Server C")

    return r.json()

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_user():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, fresh=False)
    return jsonify(access_token=new_access_token), 200

@app.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():
    db = SessionLocal()
    data = db.query(PostsY).all()
    posts_y = [k.to_dict() for k in data]
    return jsonify(posts_y=posts_y)

@app.route("/posts", methods=["POST"])
@jwt_required()
def create_a_post():
    post_info = request.get_json(silent=True) or {}
    current_user = get_jwt_identity()
    post = post_info.get("post", "")

    created = create_post(account_id=current_user, post=post)
    if created.error_message:
        return jsonify(message=created.error_message)
    return jsonify(message='Post saved', post=post)

@app.route("/likes", methods=["POST"])
@jwt_required()
def like_a_post():
    like_info = request.get_json(silent=True) or {}
    post_id = like_info.get("post_id", "")
    current_user = get_jwt_identity()

    created = like_post(post_id=post_id, account_id=current_user)
    if created.error_message:
        return jsonify(message=created.error_message)

    db = SessionLocal()
    number_of_likes = db.query(LikesY).filter_by(post_id=post_id).count()
    return jsonify(message='Post liked', number_of_likes=number_of_likes)

@app.route("/comments", methods=["POST"])
@jwt_required()
def comment_a_post():
    comment_info = request.get_json(silent=True) or {}
    post_id = comment_info.get("post_id", "")
    text = comment_info.get("text", "")
    current_user = get_jwt_identity()

    created = comment_post(post_id=post_id, account_id=current_user, text=text)
    if created.error_message:
        return jsonify(message=created.error_message)

    db = SessionLocal()
    post = db.query(PostsY).filter_by(post_id=post_id).first()
    comments = db.query(CommentsY).filter_by(post_id=post_id).all()
    comments_post = [{
        "comment_id": k.comment_id,
        "account_id": k.account_id,
        "time_commented": k.time_commented,
        "text": k.text}
        for k in comments]

    return jsonify(message='Comment saved', post=post.to_dict(), comments=comments_post)

@app.route("/reactions", methods=["POST"])
@jwt_required()
def react_a_post():
    rxn_info = request.get_json(silent=True) or {}
    post_id = rxn_info.get("post_id", "")
    text = rxn_info.get("reaction_text", "")
    current_user = get_jwt_identity()

    created = react_post(
        post_id=post_id, account_id=current_user, reaction_text=text)
    if created.error_message:
        return jsonify(message=created.error_message)

    return jsonify(message='Reaction saved')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# app.py

#resource: https://blog.appsignal.com/2025/04/30/using-jwts-in-python-flask-rest-framework.html

import os
import requests
from flask import Flask, request, jsonify
from database import SessionLocal
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import PostsY
from config import SERVER_C_URL 

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

@app.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():
    db = SessionLocal()
    data = db.query(PostsY).all()
    posts_y = [{
            "post_id": k.post_id,
            "account_id": k.account_id,
            "time_created": k.time_created,
            "post": k.post}
        for k in data]     
    return jsonify(posts_y=posts_y)    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


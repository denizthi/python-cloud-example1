
import os
import requests
from flask import Flask, request, jsonify
from database import SessionLocal
from dotenv import load_dotenv
from models import PostsY

app = Flask(__name__)
load_dotenv()
SERVER_C_URL = os.getenv("C_URL")


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
    json_cred = request.get_json(silent=True)
    
    try:
        r = requests.post((str(SERVER_C_URL) + "/login"), json=json_cred)
    except requests.RequestException:
            return jsonify(error="Cannot reach Server C")

    return r.content

@app.route("/posts", methods=["GET"])
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
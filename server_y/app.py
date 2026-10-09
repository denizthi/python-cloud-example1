from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
import psycopg

load_dotenv()
database_url = os.environ["DATABASE_URL"]
server_c_url = os.environ["C_URL"]

app = Flask(__name__)

@app.route('/status')
def status():
    return 'I am Server Y'

@app.route("/new_user", methods=["POST"])
def new_user():
    json_cred = request.get_json(silent=True)
    
    try:
        r = requests.post((str(server_c_url) + "/new_user"), json=json_cred)
    except requests.RequestException:
            return jsonify(error="Cannot reach Server C")

    return r.content

@app.route("/login", methods=["POST"])
def login():
    json_cred = request.get_json(silent=True)
    
    try:
        r = requests.post((str(server_c_url) + "/login"), json=json_cred)
    except requests.RequestException:
            return jsonify(error="Cannot reach Server C")

    return r.content

@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        with psycopg.connect(database_url) as conn:
            data = conn.execute("""
                SELECT post_id, account_id, time_created, post
                FROM posts_y
                ORDER BY post_id
                """).fetchall()
    except psycopg.Error:
        return jsonify(error="Cannot load posts.")

    posts_y = [{
            "post_id": k[0],
            "account_id": k[1],
            "time_created": k[2],
            "post": k[3]}
        for k in data]

    return jsonify(posts=posts_y)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
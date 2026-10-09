from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg
import os
import uuid

from dotenv import load_dotenv

load_dotenv()
database_url = os.environ["DATABASE_URL"]

app = Flask(__name__)

@app.route('/status')
def status():
    return 'I am Server C'

@app.route('/new_user', methods=['POST'])
def new_user():
    credentials = request.get_json(silent=True) or {}
    email = credentials.get("email", "")
    password = credentials.get("password", "")

    if not email or not password:
        return jsonify(error="Check your email and password")
    
    if len(email) > 50:
        return jsonify(error="Your email is too long")

    try:
        account_id = uuid.uuid4()
        password_hash = generate_password_hash(password)

        with psycopg.connect(database_url) as conn:
            conn.execute("""
                INSERT INTO accounts (account_id, email, password_hash)
                VALUES (%s, %s, %s)""", (account_id, email, password_hash))
            
    except psycopg.errors.UniqueViolation:
        return jsonify(message="User already exists")

    return jsonify(message="New user registered", account_id=str(account_id))

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json(silent=True) or {}
    email = credentials.get("email", "")
    password = credentials.get("password", "")
    
    if not email or not password:
        return jsonify(error="Check your email and password")

    with psycopg.connect(database_url) as conn:
            account = conn.execute(
                "SELECT account_id, password_hash FROM accounts WHERE email = %s", 
                (email,)).fetchone()

    if not account:
        return jsonify(error="Check your email and password")
    if check_password_hash(account[1], password) == False:
        return jsonify(error="Check your password")
    
    return jsonify(message="Login successful", account_id=str(account[0]))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
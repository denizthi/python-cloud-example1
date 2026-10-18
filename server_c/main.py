from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
import os
import uuid

import user_services

from user_services import create_user, confirm_token, login
from config import mail
from models import Account

from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config.from_pyfile("config.py")
mail.init_app(app)

jwt = JWTManager(app)

@app.route('/status')
def status():
    return 'I am Server C'

@app.route('/new_user', methods=['POST'])
def new_user():
    credentials = request.get_json(silent=True) or {}
    email = credentials.get("email", "")
    password = credentials.get("password", "")

    new_user = create_user(email, password)
    if new_user.has_error():
        return jsonify(message=new_user.error_message)

    return jsonify(message="Please check your email for the verification link", account_id=str(new_user.account_id))

@app.route("/verify/<token>")
def verify_email(token): 
    email = confirm_token(token)
    if not email:
        return "Invalid or expired verification link."
    
    db = SessionLocal()

    user = db.query(Account).filter_by(email=email).first()
    if user and not user.is_verified:
        user.is_verified = True
        db.commit()
        return "Your account has been verified!"
    else:
        return "Account already verified."

@app.route('/login', methods=['POST'])
def logged_user():
    credentials = request.get_json(silent=True) or {}
    email = credentials.get("email", "")
    password = credentials.get("password", "")

    user = login(email, password)
    if user.has_error():
        return jsonify(message=user.error_message)

    log_token = create_access_token(identity=user.account_id)

    return jsonify(message="Login successful", log_token=log_token)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

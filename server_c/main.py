import jwt as pyjwt
import requests 
from flask import Flask, request, jsonify
from database import SessionLocal

from email_verif import confirm_token
from user_services import create_user, login
from config import mail
from models import Account
from dotenv import load_dotenv
from config import JWT_SECRET_KEY, X_URL, Y_URL

from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

app = Flask(__name__)
load_dotenv()
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

    return jsonify(message="Please check your email for the verification link", account_id=str(new_user.account_id)), 200

@app.route("/verify/<token>")
def verify_email(token): 
    email = confirm_token(token)
    if not email:
        return "Invalid or expired verification link.", 401
    
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
    sender_info = credentials.get("sender", "")

    user = login(email, password)
    if user.has_error():
        return jsonify(message=user.error_message), 401

    app_claims = {"scope": "application", "sender": sender_info}
    cloud_claims = {"scope": "cloud", "sender": sender_info}

    app_token = create_access_token(identity=user.account_id, additional_claims=app_claims)
    cloud_token = create_access_token(identity=user.account_id, additional_claims=cloud_claims)

    return jsonify(message="Login successful", app_token=app_token, cloud_token=cloud_token), 200

@app.route('/sync', methods=['POST'])
@jwt_required()
def sync_and_post():
    checking_jwt = get_jwt()
    if checking_jwt.get("scope") != "cloud":
        return jsonify(error= "Requires cloud token"), 403
   
    cloud_token = request.headers["Authorization"]
    data = request.get_json(silent=True) or {}
    platform = data.get("platform", "")
    
    if platform == "server_x":
        try:
            headers = {"Authorization": cloud_token}
            r = requests.post((str(X_URL) + "/internal"), json=data, timeout=10, headers=headers)
        except requests.RequestException:
            return jsonify(error="Cannot reach Server X")
    elif platform == "server_y":
        try:
            headers = {"Authorization": cloud_token}
            r = requests.post((str(Y_URL) + "/internal"), json=data, timeout=10, headers=headers)
        except requests.RequestException:
            return jsonify(error="Cannot reach Server Y")
    else:
        return jsonify(error="Bad request"), 400
    
    return r.json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# user_services

import uuid

from dataclasses import dataclass

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

from database import SessionLocal
from models import Account
from email_verif import generate_token, send_verification_email

@dataclass
class CreateUserResponse:
    account_id: uuid.UUID | None = None
    verify_url: str | None = None
    error_message: str | None = None

    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False

@dataclass
class LoginResponse:
    account_id: uuid.UUID | None = None
    error_message: str | None = None
    
    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False

def create_user(email: str, password: str) -> CreateUserResponse:
    if not email or not password:
        return CreateUserResponse(error_message="Check your email and password")

    if len(email) > 50:
        return CreateUserResponse(error_message="Your email is too long")

    db = SessionLocal()
    if db.query(Account).filter_by(email=email).first():
        return CreateUserResponse(error_message="User already exists")

    account_id = uuid.uuid4()
    password_hash = generate_password_hash(password)


    new_account = Account(account_id=account_id,
                          email=email, password_hash=password_hash)
    db.add(new_account)
    db.commit()

    token = generate_token(email)
    verify_url = url_for("verify_email", token=token, _external=True)
    send_verification_email(email, verify_url)

    return CreateUserResponse(account_id=account_id, verify_url=verify_url)

def login(email: str, password: str) -> LoginResponse:
    if not email or not password:
        return LoginResponse(error_message="Check your email and password")

    db=SessionLocal()
    account = db.query(Account).filter_by(email=email).first()

    if not account:
        return LoginResponse(error_message="User does not exist")

    if not check_password_hash(account.password_hash, password):
        return LoginResponse(error_message="Check your email and password")

    return LoginResponse(account_id=account.account_id)
    
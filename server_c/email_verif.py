# email_verif

# resource: https://mailtrap.io/blog/flask-email-verification/v

import logging
import traceback
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from config import SECRET_KEY, mail


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

s = URLSafeTimedSerializer(SECRET_KEY)

def generate_token(email):
    return s.dumps(email, salt="email-confirm")

def confirm_token(token, expiration=3600):
    try:
        return s.loads(token, salt="email-confirm", max_age=expiration)
    except SignatureExpired:
        logging.warning("Verification token expired.")
        return False
    except BadSignature:
        logging.warning("Invalid verification token.")
        return False 

def send_verification_email(to, verify_url):
    try:
        msg = Message(
            subject="Verify Your Account",
            recipients=[to],
            html=f"""
            <p>Click the link below to verify your email:</p>
            <p><a href="{verify_url}">{verify_url}</a></p>
            """
        )
        mail.send(msg)
        logging.info(f"Verification email sent to {to}.")
    except Exception as e:
        logging.error(f"Error sending email to {to}: {str(e)}")
        logging.error(traceback.format_exc())
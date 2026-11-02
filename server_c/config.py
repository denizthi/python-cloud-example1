# confic.py

import os
from dotenv import load_dotenv
from flask_mail import Mail
from datetime import timedelta
 
mail = Mail()

load_dotenv()

SECRET_KEY = os.getenv("secret_key")
JWT_SECRET_KEY = os.getenv("jwt_secret_key_c")
MAIL_SERVER = os.getenv("MAIL_SERVER", "live.smtp.mailtrap.io")
MAIL_PORT = os.getenv("MAIL_PORT", 587 )
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = "no-reply@demomailtrap.co"

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

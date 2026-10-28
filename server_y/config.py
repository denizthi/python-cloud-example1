# confic.py

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

SERVER_C_URL = os.getenv("C_URL")
SECRET_KEY = os.getenv("secret_key")
JWT_SECRET_KEY = os.getenv("jwt_secret_key")

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=3)

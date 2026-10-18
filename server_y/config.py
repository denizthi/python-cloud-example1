# confic.py

import os
from dotenv import load_dotenv


load_dotenv()

SERVER_C_URL = os.getenv("C_URL")
SECRET_KEY = os.getenv("secret_key")
JWT_SECRET_KEY = os.getenv("jwt_secret_key")

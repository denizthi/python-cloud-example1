# auth.py

import os
from dataclasses import dataclass
import requests
import jwt as pyjwt

SERVER_C_URL = os.getenv("C_URL")
JWT_C = os.getenv("jwt_secret_key_c")

@dataclass
class LoginServerC:
    current_user: str | None = None
    error_message: str | None = None

    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False


def login_on_c(email: str, password: str) -> LoginServerC:
    l_user = {"email": email, "password": password}
    try:
        r = requests.post((str(SERVER_C_URL) + "/login"), json=l_user)
    except requests.RequestException:
        return LoginServerC(error_message="Cannot reach Server C")
    
    return r.json()
    
    #app_token = create_access_token(identity=current_user, fresh=True)
    #refresh_token = create_refresh_token(identity=current_user)
    #return jsonify(message="Login successful", app_token=app_token, refresh_token=refresh_token), 200


import jwt
import os
from flask import request

def get_username_from_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]
        data = jwt.decode(token, os.getenv("PRIVATE_KEY"), algorithms=["HS256"])
        return data["username"]
    except:
        return None
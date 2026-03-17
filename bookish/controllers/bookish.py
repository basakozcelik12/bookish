import datetime
import jwt
import os
from flask import request, jsonify

def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/login', methods=["POSt"])
    def get_token():
        data = request.get_json()

        username = data.get("username")

        token = jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        os.getenv("PRIVATE_KEY"),
        algorithm="HS256"
    )

        return jsonify({"access_token": token})



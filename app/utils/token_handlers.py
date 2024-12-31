import os
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt
from app.utils import static_english_data, static_arabic_data

APP_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-here")


def generate_token(user_id):
    """
    Generate a JWT token for a given user ID.

    :param user_id: Unique identifier for the user
    :return: JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        "iat": datetime.utcnow(),  # Issued at time
    }

    # Encode the token using the secret key
    token = jwt.encode(payload, APP_SECRET_KEY, algorithm="HS256")
    return token


def token_required(f):
    """
    Decorator to require a valid JWT token for route access

    :param f: Route function to wrap
    :return: Wrapped function with token verification
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if Authorization header is present
        lang = request.accept_languages.best_match(["en", "ar"])
        data = static_english_data if lang == "en" else static_arabic_data

        token = None
        if "Authorization" in request.headers:
            # Bearer TOKEN
            auth_header = request.headers["Authorization"]
            token = (
                auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
            )

        if not token:
            return jsonify({"message": data["missing_token"]}), 401

        try:
            # Decode and verify the token
            payload = jwt.decode(token, APP_SECRET_KEY, algorithms=["HS256"])
            current_user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": data["token_expired"]}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": data["invalid_token"]}), 401

        # Add the current user to the request context if needed
        return f(current_user_id, *args, **kwargs)

    return decorated

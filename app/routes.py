from flask import Blueprint, request, jsonify, g, json
from flask_babel import Babel, gettext, get_locale
from marshmallow import ValidationError
from app.utils import static_arabic_data, static_english_data
from .models import db, User
from .schemas import user_schema, users_schema
from app.utils import token_required

main = Blueprint("main", __name__)
babel = Babel()


@babel.localeselector
def get_locale():
    # Detect language from request or use default
    return request.accept_languages.best_match(["en", "ar"])


@main.route("/", methods=["GET"])
@token_required
def say_hello():
    current_language = get_locale()

    data = static_arabic_data if current_language == "ar" else static_english_data

    return jsonify({"message": data["welcome_message"]})


@main.route("/register", methods=["POST"])
def create_user():
    try:
        # Validate incoming JSON
        data = user_schema.load(request.get_json())

        print(data)
        # Check if user already exists
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"message": _("User with this email already exists")}), 400

        # Create new user
        new_user = User(username=data["username"], email=data["email"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201

    except ValidationError as err:
        return jsonify({"message": _("Validation Error"), "errors": err.messages}), 400


@main.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

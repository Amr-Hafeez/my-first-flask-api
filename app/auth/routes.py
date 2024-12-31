from flask import Blueprint, request, jsonify
from flask_babel import Babel
from marshmallow import ValidationError
from app.models import User, db
from app.schemas import user_schema, users_schema
from app.utils import modify_error_messages

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
babel = Babel()


@babel.localeselector
def get_locale():
    # Detect language from request or use default
    return request.accept_languages.best_match(["en", "ar"])


@auth_bp.route("/register", methods=["POST"])
def register():
    current_language = get_locale()
    print(f"current_language {current_language}")
    try:
        if current_language is None:
            raise ValueError("Please Provide the (Accept-Language) header")

        request_data = request.get_json()
        data = user_schema.load(request_data)

        new_user = User(
            username=request_data.get(
                "username"
            ),  # Use request_data, not the validated data
            email=request_data.get("email"),
        )
        new_user.set_password(request_data.get("password"))
        db.session.add(new_user)
        db.session.commit()
        print(data)

        return jsonify(user_schema.dump(new_user)), 201
    except ValueError as e:
        return jsonify({"error_message": str(e)}), 400
    except ValidationError as err:
        return (
            jsonify({"errors": modify_error_messages(err.messages, current_language)}),
            400,
        )


@auth_bp.route("/get-all-users", methods=["GET"])
def all_users():
    try:
        users = User.query.all()
        return jsonify({"users": users_schema.dump(users)})
    except ValueError as err:
        print(err)
        return jsonify({"errors": str(err)})

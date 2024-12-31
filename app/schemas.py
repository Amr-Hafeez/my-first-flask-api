from marshmallow import Schema, fields, validate, ValidationError
from flask_marshmallow import Marshmallow
from .models import User

ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    # id = ma.auto_field()
    # username = ma.auto_field()
    # email = ma.auto_field()
    # created_at = ma.auto_field()

    id = fields.Int(dump_only=True)  # Only included when serializing
    username = fields.Str(
        required=True,
        validate=lambda n: len(n.strip()) > 0,
        error_messages={
            "required": "field_is_required",
            "validator_failed": "field_is_empty",
        },
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "field_is_required", "invalid": "field_is_invalid"},
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=lambda p: len(p) >= 6,
        error_messages={
            "required": "field_is_required",
            "validator_failed": "password_validation_failed",
        },
    )
    createdAt = fields.DateTime(dump_only=True)

    # id = fields.Int(dump_only=True)
    # username = fields.Str(
    #     required=True,
    #     validate=validate.Length(min=3, max=50),
    #     error_messages={"required": "Username is required"},
    # )
    # email = fields.Email(
    #     required=True,
    #     validate=validate.Email(),
    #     error_messages={"invalid": "Invalid email format"},
    # )
    #
    # created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

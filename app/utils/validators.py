from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        error_messages={"required": "Username is required"},
    )
    email = fields.Email(
        required=True,
        validate=validate.Email(),
        error_messages={"invalid": "Invalid email format"},
    )
    created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

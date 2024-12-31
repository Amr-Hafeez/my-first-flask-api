from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


def handle_errors(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Validation Error",
                    "errors": error.messages,
                }
            ),
            400,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        return (
            jsonify(
                {"status": "error", "message": "Database Error", "details": str(error)}
            ),
            500,
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Resource Not Found"}), 404

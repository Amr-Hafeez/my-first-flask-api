import os
from flask import Flask
from flask_marshmallow import Marshmallow
from .models import db, migrate
from .routes import main, babel
from .auth import auth_bp
from .utils.error_handler import handle_errors
from config import Config
from dotenv import load_dotenv
from .schemas import ma

load_dotenv()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Register blueprint
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)

    # Setup error handlers
    handle_errors(app)

    # Create database tables
    # with app.app_context():
    #   db.create_all()

    print(os.getenv("PORT"))

    return app

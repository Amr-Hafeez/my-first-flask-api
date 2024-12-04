from flask import Flask
from .models import db, migrate
from .routes import main, babel
from .utils.error_handler import handle_errors
from config import Config


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  # Initialize extensions
  db.init_app(app)
  babel.init_app(app)
  migrate.init_app(app, db)

  # Register blueprint
  app.register_blueprint(main)

  # Setup error handlers
  handle_errors(app)

  # Create database tables
  # with app.app_context():
  #   db.create_all()

  return app

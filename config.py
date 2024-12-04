import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

# Base configuration that can be inherited
class Config:
  # Secret key for sessions and CSRF protection
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-key-here'

  # SQLAlchemy Database Configuration
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Application Settings
  DEBUG = False
  TESTING = False

  # Internationalization
  BABEL_DEFAULT_LOCALE = 'en'
  BABEL_DEFAULT_TIMEZONE = 'UTC'
  LANGUAGES = ['en', 'ar']

  # Security Settings
  SESSION_COOKIE_SECURE = True
  REMEMBER_COOKIE_SECURE = True

  # Pagination
  ITEMS_PER_PAGE = 10

  # Logging Configuration
  LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'false').lower() == 'true'

  # Token Expiration
  ACCESS_TOKEN_EXPIRE_MINUTES = 30

  # Env Variables
  PORT = os.environ.get('PORT') or 5000


# Development specific configurations
class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_ECHO = True  # Print SQL statements
  SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


# Production specific configurations
class ProductionConfig(Config):
  DEBUG = False
  # Use a proper production database
  SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')

  # Enhanced security for production
  SESSION_COOKIE_HTTPONLY = True
  REMEMBER_COOKIE_HTTPONLY = True

  # Stricter security settings
  SECRET_KEY = os.environ.get('PRODUCTION_SECRET_KEY')


# Testing specific configurations
class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests


# Configuration factory
def get_config(config_name):
  config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
  }
  return config_mapping.get(config_name, DevelopmentConfig)
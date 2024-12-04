from flask import Blueprint, request, jsonify, g, json
from flask_babel import Babel, gettext, get_locale
from .models import db, User
from .schemas import user_schema, users_schema
from marshmallow import ValidationError

main = Blueprint('main', __name__)
babel = Babel()


@babel.localeselector
def get_locale():
  # Detect language from request or use default
  return request.accept_languages.best_match(['en', 'ar'])


def load_static_data(language='en'):
  """Load static data from JSON files based on language"""
  filename = f'app/data/static_data_{language}.json'
  try:
    with open(filename, 'r', encoding='utf-8') as f:
      return json.load(f)
  except FileNotFoundError:
    return []


@main.route('/', methods=['GET'])
def say_hello():
  current_language = get_locale();
  print(current_language)
  data = load_static_data(current_language)
  return jsonify({'message': data["welcome_message"]})


@main.route('/users', methods=['POST'])
def create_user():
  try:
    # Validate incoming JSON
    data = user_schema.load(request.get_json())

    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
      return jsonify({
        'message': _('User with this email already exists')
      }), 400

    # Create new user
    new_user = User(
      username=data['username'],
      email=data['email']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201

  except ValidationError as err:
    return jsonify({
      'message': _('Validation Error'),
      'errors': err.messages
    }), 400


@main.route('/users', methods=['GET'])
def get_users():
  users = User.query.all()
  return jsonify(users_schema.dump(users))
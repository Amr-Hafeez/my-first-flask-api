from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()



# class User(db.Model):
#   __tablename__ = 'users'
#
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(50), unique=True, nullable=False)
#   email = db.Column(db.String(120), unique=True, nullable=False)
#   created_at = db.Column(db.DateTime, default=datetime.utcnow)
#
#   @validates('email')
#   def validate_email(self, key, email):
#     assert '@' in email, 'Invalid email address'
#     return email
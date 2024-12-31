from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy.orm import validates
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    post = db.relationship("Post", backref="author", lazy="dynamic")

    # Defines how python will print objects of this class.
    def __repr__(self):
        # the '%r' works as a placeholder.
        return "<User %r>" % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post %r>" % self.body


#   @validates('email')
#   def validate_email(self, key, email):
#     assert '@' in email, 'Invalid email address'
#     return email

"""Models for Feedback app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20))
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return f"<User {self.username} password={self.password} email={self.email} first_name={self.first_name} last_name={self.last_name}>"

    def serialize(self):
        """Returns a dictionary representation of a user's info."""

        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

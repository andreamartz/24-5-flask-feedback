"""Models for Feedback app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """Register user with hashed password and return the user."""

        # take in a password and turn it into a hash;
        # bcrypt returns that massive string which is a bytestring
        hashed = bcrypt.generate_password_hash(pwd)

        # turn bytestring into normal (unicode UTF8) string that we can store in our database
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        u = User.query.filter_by(username=username).first()

        # Look for a user with that username.
        if u and bcrypt.check_password_hash(u.password, pwd):
            # If user is found, return user instance
            return u

        # If no user found, return false.
        else:
            return False

    def __repr__(self):
        return f"<User {self.username} password={self.password} email={self.email} first_name={self.first_name} last_name={self.last_name}>"


class Post(db.Model):
    """User model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey(
        'users.username'), nullable=False)

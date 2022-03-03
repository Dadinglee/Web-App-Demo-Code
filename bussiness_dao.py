"""Bussiness models"""

import flask_login
from sqlalchemy import TypeDecorator, Text
from app_factory import db
from password_hash import PasswordHash


class Password(TypeDecorator):
    """Allows storing and retrieving password hashes using PasswordHash."""

    impl = Text

    def __init__(self, rounds=12, **kwds):
        self.rounds = rounds
        super(Password, self).__init__(**kwds)

    def process_bind_param(self, value, dialect):
        """Ensure the value is a PasswordHash and then return its hash."""
        return self._convert(value).hash

    def process_result_value(self, value, dialect):
        """Convert the hash to a PasswordHash, if it's non-NULL."""
        if value is not None:
            print(value)
            return PasswordHash(value)

    def process_literal_param(self, value, dialect):
        return super().process_literal_param(value, dialect)

    def validator(self, password):
        """Provides a validator/converter for @validates usage."""
        return self._convert(password)

    def _convert(self, value):
        """Returns a PasswordHash from the given string.

        PasswordHash instances or None values will return unchanged.
        Strings will be hashed and the resulting PasswordHash returned.
        Any other input will result in a TypeError.
        """
        if isinstance(value, PasswordHash):
            return value
        elif isinstance(value, str):
            return PasswordHash.new(value, self.rounds)
        elif value is not None:
            raise TypeError("Cannot convert {} to a PasswordHash".format(type(value)))


class User(flask_login.UserMixin, db.Model):
    """User model to store password, username

    Args:
        flask_login (_type_): _description_
        db (_type_): _description_
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(Password, unique=False, nullable=False)


class Review(db.Model):
    """Review model to store comments and ratings

    Args:
        db (_type_): _description_
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    rate = db.Column(db.Integer)
    comment = db.Column(db.String(200), nullable=True)
    movie_id = db.Column(db.String(20), nullable=False)

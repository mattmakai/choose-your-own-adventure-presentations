from flask import url_for
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(UserMixin, db.Model):
    """
        Represents an admin user in cyoa.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


class Presentation(db.Model):
    """
        Contains data regarding a single presentation.
    """
    __tablename__ = 'presentations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    filename = db.Column(db.String(256))
    url_slug = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)
    choices_number = db.Column(db.String(32), default="")
    choices_email = db.Column(db.String(40), default="")
    choices = db.relationship('Choice', lazy='dynamic')

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def __repr__(self):
        return '<Presentation %r>' % self.name


class Choice(db.Model):
    """
        A branch in the storyline that an audience member can vote on.
        Maps directly into what is stored in Redis.
    """
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    votes = db.Column(db.Integer, default=0)
    presentation = db.Column(db.Integer, db.ForeignKey('presentations.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Choice %r>' % self.name


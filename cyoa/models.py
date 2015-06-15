from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Wizard(UserMixin, db.Model):
    """
        Represents a wizard who can access special parts of the application.
    """
    __tablename__ = 'wizards'
    id = db.Column(db.Integer, primary_key=True)
    wizard_name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, wizard_name, password):
        self.wizard_name = wizard_name
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
        return '<Wizard %r>' % self.wizard_name


class Presentation(db.Model):
    """
        Contains data regarding a single presentation.
    """
    __tablename__ = 'presentations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(128), unique=True)
    filename = db.Column(db.String(256))
    is_visible = db.Column(db.Boolean, default=False)
    decisions = db.relationship('Decision', lazy='dynamic')

    def __repr__(self):
        return '<Presentation %r>' % self.name


class Decision(db.Model):
    """
        A branch in the storyline that an audience member can vote on.
        Must map directly into what is stored in Redis.
    """
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(128))
    first_path_slug = db.Column(db.String(128))
    second_path_slug = db.Column(db.String(128))
    presentation = db.Column(db.Integer, db.ForeignKey('presentations.id'))

    def __repr__(self):
        return '<Decision %r>' % self.slug

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required(), 
                                                     Length(1, 32)])

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None and not user.verify_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        return True


class PresentationForm(Form):
    name = StringField('Presentation name', validators=[Required(), 
                                                        Length(1, 60)])
    filename = StringField('File name', validators=[Required(), 
                                                    Length(1, 255)])
    is_active = BooleanField()
    number = StringField('Text-in phone number', validators=[Length(8, 32)])
    email = StringField('Text-in email address', validators=[Length(4, 40),
                                                             Email()])
    choices = StringField('Choices (semicolon delimited)', 
                          validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        f = Presentation.query.filter_by(filename=self.filename.data).first()
        if f is not None:
            self.filename.append('File name must be new and unique.')
            return False
        return True

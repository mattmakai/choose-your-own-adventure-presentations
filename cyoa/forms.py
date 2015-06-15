from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    DateField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from .models import Wizard


class LoginForm(Form):
    wizard_name = StringField('Wizard Name',
                              validators=[Required(), Length(1, 32)])
    password = PasswordField('Password', validators=[Required(),
                                                     Length(1, 32)])

    def validate(self):
        if not Form.validate(self):
            return False
        user = Wizard.query.filter_by(wizard_name=self.
                                      wizard_name.data).first()
        if user is not None and not user.verify_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        return True


class PresentationForm(Form):
    name = StringField('Presentation name', validators=[Required(),
                                                        Length(1, 60)])
    filename = StringField('File name', validators=[Required(),
                                                    Length(1, 255)])
    slug = StringField('URL slug', validators=[Required(),
                                               Length(1, 255)])
    is_visible = BooleanField()


class DecisionForm(Form):
    slug = StringField('URL slug', validators=[Required(),
                                               Length(1, 128)])
    first_path_slug = StringField('A word for the first path. Must be '
                                  'lowercase. No spaces.',
                                  validators=[Required(), Length(1, 64),
                                              Regexp('[a-z0-9]+', message=
                                              'Choice must be lowercase '
                                              'with no whitespace.')])
    second_path_slug = StringField('A word for the second path. Must be '
                                   'lowercase. No spaces.',
                                   validators=[Required(), Length(1, 64),
                                               Regexp('[a-z-0-9]+', message=
                                               'Choice must be lowercase '
                                               'with no whitespace.')])

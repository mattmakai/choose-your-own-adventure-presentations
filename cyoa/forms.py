from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    DateField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from .models import Wizard, Presentation


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
    is_active = BooleanField()
    voting_number = StringField('Text-in phone number',
                                validators=[Length(0, 32)])
    enable_browser_voting = BooleanField()


class ChoiceForm(Form):
    name = StringField('Voting choice name', validators=[Required(),
                                                        Length(1, 60)])
    slug = StringField('URL slug', validators=[Required(),
                                               Length(1, 60)])
    decision_point = IntegerField('Decision Point #', validators=[Required()])

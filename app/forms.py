# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.fields import TextAreaField  # Import TextAreaField explicitly
from .models import User, Organization  # Import Organization model

class RegistrationForm(FlaskForm):
    userId = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone')
    organization_name = StringField('Organization Name', validators=[DataRequired()])
    organization_description = TextAreaField('Organization Description')  # Added organization description field
    submit = SubmitField('Sign Up')

    def validate_userId(self, userId):
        user = User.query.filter_by(userId=userId.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already registered.')

class LoginForm(FlaskForm):
    userId = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')




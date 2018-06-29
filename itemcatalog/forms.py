from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from dbmodels import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired("Username is required")])
    email = StringField('Email', validators=[
                        DataRequired("You must enter email address"), Email("Enter valid email address")])
    password = PasswordField('Password', validators=[
                             DataRequired("Password is required")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired("You must repeat password"),
                                       EqualTo('password', "Passwords must match")])
    submit = SubmitField('Register')

    def validate_email(self, email):
        emailad = User.query.filter_by(email=email.data).first()
        if emailad is not None:
            raise ValidationError('Please use a different email address.')

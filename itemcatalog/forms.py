from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from dbmodels import User, Password


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
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address has been registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired("You must enter an email address"), Email("Enter valid email address")])
    password = PasswordField('Password', validators=[
                             DataRequired("Password is required")])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Invalid email address or password")
        else:
            # if the user exists in the user table, they may have authenticated with Google,
            # Check the password table to see if they even have a password
            psw = Password.query.filter_by(userid=user.id).first()
            if psw is None:
                raise ValidationError(
                    "Try Logging in with your google account :)")


class newItemForm(FlaskForm):
    name = StringField('Item Name', validators=[
                       DataRequired("You must enter the name of the item")])
    description = TextAreaField('Description', validators=[
                                DataRequired("You must enter a description for theitem")])
    category = SelectField('Category', choices=[], validators=[
                           DataRequired("Please select a category")])
    submit = SubmitField('Create Item')

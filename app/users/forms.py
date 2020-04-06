from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # costume validator for username
    def validating_username(self, username):
        # print(":::::::::::::::::", username.data)
        # print(":::::::::::::::::", User.query.filter_by(username=username.data).first())
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Choose another things')

    # costume validator for email
    def validating_email(self, email):
        # print(":::::::::::::::::", email.data)
        # print(":::::::::::::::::", User.query.filter_by(email=email.data).first())
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is already taken. Choose another things')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # profile pic update
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # costume validator for username
    def validating_username(self, username):
        print("::::::::1:::::::::", username.data)
        print("::::::::2:::::::::", current_user.username)
        print("::::::::3:::::::::", User.query.filter_by(username=username.data).first())
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            print("::::::4:::::::::::", user)
            if user:
                raise ValidationError('Username is already taken. Choose another things')

    # costume validator for email
    def validateing_email(self, email):
        print(":::::::::::::::::", email.data)
        print(":::::::::::::::::", User.query.filter_by(email=email.data).first())
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email is already taken. Choose another things')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



# requesting password reset page
class ResetPasswordRequestFrom(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Password reset request')

    # costume validator for email
    def validating_email(self, email):
        # print(":::::::::::::::::", email.data)
        # print(":::::::::::::::::", User.query.filter_by(email=email.data).first())
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("You don't have any account here. Try another one or Register first")


# Resetting password page
class PasswordResetFrom(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
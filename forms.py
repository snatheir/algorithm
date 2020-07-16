from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields.html5 import EmailField
from wtforms import validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 

    email = EmailField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class algorithmForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class submitAlgorithmForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=10000)])
    inputJSON = StringField('Input Required (JSON)', validators=[DataRequired(), Length(min=2, max=500)]) 
    outputJSON = StringField('Output Produced (JSON)', validators=[DataRequired(), Length(min=2, max=500)])

    submit = SubmitField('Login')
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


class AlgorithmForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=10000)])
    sample_input = StringField('Input Required (JSON)', validators=[DataRequired(), Length(min=2, max=500)]) 
    sample_output = StringField('Output Produced (JSON)', validators=[DataRequired(), Length(min=2, max=500)])
    tags = ListField(StringField(default=[]))
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    pass


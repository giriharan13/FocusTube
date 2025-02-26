from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,EqualTo

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")


class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=5)])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=5)])
    login = SubmitField("Login")


class SignUpForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=5)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    signup = SubmitField("Signup")
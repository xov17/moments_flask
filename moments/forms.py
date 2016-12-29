from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    firstname = StringField('firstname', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('email', validators=[DataRequired(), Email()])

class SignInForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])

class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired(), Length(min=1, max=200)])
# -*- encoding: utf-8 -*-
"""
Light Bootstrap Dashboard - coded in Flask

Author  : AppSeed App Generator
Design  : Creative-Tim.com
License : MIT 
Support : https://appseed.us/support 
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, DateField
from wtforms.fields		import DateField
from wtforms.validators import InputRequired, Email, DataRequired, Length

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired(), Length(min=4, max=20)])
	password    = PasswordField(u'Password'        , validators=[DataRequired(), Length(min=6, max=50)])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired(), Length(min=4, max=20)])
	password    = PasswordField(u'Password'  , validators=[DataRequired(), Length(min=6, max=50)])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email(), Length(min=6, max=50)])

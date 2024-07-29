from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from website.models import User
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Username must be between 3 and 15 characters long')])
    
    first_name = StringField('First Name', validators=[DataRequired(message="Cannot leave field empty!"), Regexp('^[a-z A-Z]+$', message='Please enter only letters')])
    last_name = StringField('Last Name', validators=[DataRequired(message="Cannot leave field empty!"), Regexp('^[a-z A-Z]+$', message='Please enter only letters')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter an email (eg. TEXT123@EMAIL.com)')])
    
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^(?=.*\d).{5,15}$', message='Your password should be between 5 and 15 characters long, and contain one number.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="Cannot leave field empty!"), EqualTo('password', message='Must be equal to password')])
    
    submit = SubmitField('Register')
    

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose a different one.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is already associated with an account.')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Cannot leave field empty!"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="Cannot leave field empty!")])
    submit = SubmitField('Login')

            


class CheckoutForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Regexp('^[a-z A-Z]+$', message='Please enter only letters')])
    last_name = StringField('Last Name', validators=[DataRequired(), Regexp('^[a-z A-Z]+$', message='Please enter only letters')])
    
    card_number = StringField('Credit Card Number (16 digit number)', validators=[DataRequired(), Regexp('(\d{16})', message="Please enter a valid CC number")])
    security_number = StringField('CVV Number (3-4 digit number)', validators=[DataRequired(), Regexp('(\d{3,4})', message="Please enter a valid CVV number")])
    
    expiration_year = IntegerField('Expiration Year', validators=[DataRequired(message="Please enter only numbers"), NumberRange(min=2021, max=2031, message='Please enter a valid expiration year')])
    expiration_month = IntegerField('Expiration Month', validators=[DataRequired(message="Please enter only numbers"), NumberRange(min=1, max=12, message='Please enter a valid expiration month')])
    
    billing_adress = StringField('Billing Adress', validators=[DataRequired()])
    delivery_adress = StringField('Delivery Adress', validators=[DataRequired()])
    
    submit = SubmitField('Confirm Payment')
                



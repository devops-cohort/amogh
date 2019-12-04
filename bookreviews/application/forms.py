from flask_wtf import FlaskForm
from flask_login import LoginManager, current_user
from wtforms import BooleanField, SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application import app
from application.models import Users

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class ReviewsForm(FlaskForm):
    title = StringField('Title',
            validators=[DataRequired(), Length(min=4, max=100)])

    author = StringField('Author',
             validators=[DataRequired(), Length(min=4, max=100)])

    rating = IntegerField('Rating',
             validators=[DataRequired()])

    review = StringField('Review',
             validators=[DataRequired(), Length(min=4, max=100)])
    
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
               validators=[DataRequired()])
                                        
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    first_name = StringField('First name',
                 validators=[DataRequired(), Length(min=4, max=100)])

    last_name = StringField('Last name',
                validators=[DataRequired(), Length(min=4, max=100)])

    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
               validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                       validators= [DataRequired(), EqualTo('password')])
                                                
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use!')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                 validators=[DataRequired(), Length(min=4, max=30)])

    last_name = StringField('Last Name',
                validators=[DataRequired(), Length(min=4, max=30)])

    email = StringField('Email',
            validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already in use!')




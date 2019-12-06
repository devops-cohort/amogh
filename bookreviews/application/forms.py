from flask_wtf import FlaskForm
from flask_login import LoginManager, current_user
from wtforms import SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from application import app
from application.models import Users

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class ReviewsForm(FlaskForm):
    title = StringField('Title',
            validators=[DataRequired(), Length(min=1, max=50)])

    author = StringField('Author',
             validators=[DataRequired(), Length(min=1, max=50)])

    rating = IntegerField('Rating',
             validators=[DataRequired(), NumberRange(min=0, max=10)])

    review = StringField('Review',
             validators=[DataRequired(), Length(min=1, max=500)])
    
    submit = SubmitField('Submit')

    update = SubmitField('Update')

    delete = SubmitField('Delete review')

class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
               validators=[DataRequired()])
    
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    first_name = StringField('First name',
                 validators=[DataRequired(), Length(min=1, max=50)])

    last_name = StringField('Last name',
                validators=[DataRequired(), Length(min=1, max=50)])

    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=1, max=50)])

    password = PasswordField('Password',
               validators=[DataRequired(), Length(min=1, max=150)])

    confirm_password = PasswordField('Confirm Password',
                       validators= [DataRequired(), EqualTo('password')])
                                                
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use!')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                 validators=[DataRequired(), Length(min=1, max=50)])

    last_name = StringField('Last Name',
                validators=[DataRequired(), Length(min=1, max=50)])

    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=1, max=50)])

    update = SubmitField('Update')

    delete = SubmitField('Delete account')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already in use!')




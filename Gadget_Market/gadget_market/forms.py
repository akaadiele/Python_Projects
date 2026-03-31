# ------------------------------------------------------------------------------
# Flask Forms
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import necessary modules and classes for creating forms in Flask
from flask_wtf import FlaskForm  # Import the FlaskForm class from the flask_wtf module

from wtforms import StringField, PasswordField, SubmitField  # Import form field types from wtforms
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError  # Import validators from wtforms

from gadget_market.models import User  # Import the User model from the gadget_market package

# ------------------------------------------------------------------------------
# Register Form
class RegisterForm(FlaskForm):   # Define a form class for user registration that inherits from FlaskForm

    # Function to validate the username field
    def validate_username(self, username_to_check):  # Define a custom validation method for the username field
        user_with_username = User.query.filter_by(username=username_to_check.data).first()  # Query the database to check if a user with the given username already exists
        if user_with_username:  # If a user with the given username is found in the database
            raise ValidationError('Username already exists! Please try a different username.')  # Raise a validation error if the username already exists

    # Function to validate the email field
    def validate_email(self, email_to_check):  # Define a custom validation method for the email field
        user_with_email = User.query.filter_by(email=email_to_check.data).first()   # Query the database to check if a user with the given email already exists
        if user_with_email:  # If a user with the given email is found in the database
            raise ValidationError('Email already exists! Please try a different email address.')  # Raise a validation error if the email already exists

    # using the function name format: validate_<field_name> to create custom validation methods for the <field_name> field in the form. 
    # These methods will be automatically called by Flask-WTF when validating the form, and they will check against the <field_name> field's data to perform custom validation logic (e.g., checking for existing usernames or emails in the database). 
    # If the validation fails, a ValidationError is raised with an appropriate error message.
    
    # Define form fields with labels and validators
    username = StringField(label='Username:', validators=[Length(min=5, max=30), DataRequired()])   # Define a string field for the username input
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])   # Define a string field for the email address input
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])   # Define a password field for the password input
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])   # Define a password field for confirming the password input
    submit = SubmitField(label='Register Account')   # Define a submit button for the form

# ------------------------------------------------------------------------------
# Login Form
class LoginForm(FlaskForm):   # Define a form class for user login that inherits from FlaskForm
    # Define form fields with labels and validators
    username = StringField(label='Username:', validators=[DataRequired()])   # Define a string field for the username input
    password = PasswordField(label='Password:', validators=[DataRequired()])   # Define a password field for the password input
    submit = SubmitField(label='Sign in')   # Define a submit button for the form

# ------------------------------------------------------------------------------
# Purchase Item Form
class PurchaseItemForm(FlaskForm):   # Define a form class for purchasing an item that inherits from FlaskForm
    # Define the submit button for the form 
    submit = SubmitField(label='Purchase Item')   # Define a submit button for the form

# ------------------------------------------------------------------------------
# Sell Item Form
class SellItemForm(FlaskForm):   # Define a form class for selling an item that inherits from FlaskForm
    # Define the submit button for the form 
    submit = SubmitField(label='Sell Item')   # Define a submit button for the form
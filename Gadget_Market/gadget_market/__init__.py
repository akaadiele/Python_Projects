# ------------------------------------------------------------------------------
# Flask Application Initialization
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Importing Modules
from flask import Flask     # Import the Flask module
from flask_sqlalchemy import SQLAlchemy     # Import SQLAlchemy for database management
from flask_bcrypt import Bcrypt   # Import Bcrypt for password hashing
from flask_login import LoginManager   # Import LoginManager for user session management and authentication

# ------------------------------------------------------------------------------
# Initialize essentials

# Flask application
app = Flask(__name__)       # Create a Flask web server instance / Initialize the Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gadget_market.db'   # Configure the database URI
app.config['SECRET_KEY'] =  '8db3ad2f798ef921ed627511'  # Set a secret key for the application (used for forms, session management and other security features)

# Database
db = SQLAlchemy(app)     # Initialize the SQLAlchemy extension with the Flask app

# Bcrypt
bcrypt = Bcrypt(app)     # Initialize the Bcrypt extension with the Flask app

# Login Manager
login_manager = LoginManager(app)   # Initialize the LoginManager extension with the Flask app
login_manager.login_view = 'login_page'  # Set the login view to the route name 'login_page' (the route that handles user login)
login_manager.login_message_category = 'info'  # Set the category for the flash message that is displayed when an unauthenticated user tries to access a protected route (optional, default is 'message')

# ------------------------------------------------------------------------------
# Import routes
from gadget_market import routes    # Import the routes module from the 'gadget_market' package

# ------------------------------------------------------------------------------

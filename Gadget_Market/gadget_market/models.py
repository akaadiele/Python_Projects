# ------------------------------------------------------------------------------
# Database Models
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import necessary modules and components
from gadget_market import db  # Import the SQLAlchemy database instance from the gadget_market package
from gadget_market import bcrypt  # Import the Bcrypt instance from the gadget_market package
from gadget_market import login_manager  # Import the LoginManager instance from the gadget_market package

from flask_login import UserMixin  # Import the UserMixin class from the flask_login module for user authentication and session management

# ------------------------------------------------------------------------------
# User Loader Function for Flask-Login
# This function is used by Flask-Login to load a user from the database based on the user ID stored in the session. It is decorated with @login_manager.user_loader to indicate that it is the user loader function for Flask-Login.
@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)    # Query the database to retrieve the user with the given user ID and return the user object
    return User.query.get(int(user_id))  # Query the database to retrieve the user with the given user ID and return the user object (using SQLAlchemy's query.get() method)

# ------------------------------------------------------------------------------
# User Model
class User(db.Model, UserMixin):   # Define a database model for users in the market that inherits from db.Model and UserMixin
    # Define the columns for the User model
    id = db.Column(db.Integer, primary_key=True)   # Primary key column
    username = db.Column(db.String(length=35), nullable=False, unique=True)   # Username column
    password_hash = db.Column(db.String(length=60), nullable=False)   # Password_hash column
    email = db.Column(db.String(length=60), nullable=False, unique=True)   # Email column
    budget = db.Column(db.Float, nullable=False, default=1000)   # Budget column
    items = db.relationship('Item', backref='owned_user', lazy=True)   # Relationship to the Item model

    def __repr__(self):   # Define a string representation for the User model
        return f"User {self.username}"
    
    # Property to format the budget with comma separators for thousands
    @property
    def formatted_budget(self):
        return f"{self.budget:,.2f}"

    # Property and setter for the password field to handle password hashing and verification. The password is not stored in the database, but the password_hash is stored instead. The setter hashes the plain text password before storing it in the database, and the check_password method verifies if a given plain text password matches the stored hashed password.
    @property
    def password(self):   # Define a property for the password field (not stored in the database)
        return self.password

    @password.setter
    def password(self, plain_text_password):   # Define a setter for the password property to hash the password before storing it in the database
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')  # Hash the plain text password and store it in the password_hash column
    
    def check_password(self, attempted_password):   # Define a method to check if the attempted password matches the stored hashed password
        try:
            return bcrypt.check_password_hash(self.password_hash, attempted_password)
        except:
            # Check if the attempted password matches the stored hashed password using bcrypt's check_password_hash function. 
            # If there is an error (e.g., if the password_hash is not set), return False to
            return False
    
    def can_purchase(self, item_obj):   # Define a method to check if the user has enough budget to purchase an item
        return self.budget >= item_obj.price  # Return True if the user's budget is greater than or equal to the price of the item, otherwise return False
    
    def can_sell(self, item_obj):   # Define a method to check if the user can sell an item (i.e., if they own the item)
        return item_obj in self.items  # Return True if the item is in the user's items (i.e., they own the item), otherwise return False

    # Inheriting from the class - UserMixin
    # The methods for is_authenticated, is_active, is_anonymous, and get_id are provided by the UserMixin class, which we have inherited in our User model.

# ------------------------------------------------------------------------------
# Item Model
class Item(db.Model):   # Define a database model for items in the market
    # Define the columns for the Item model
    id = db.Column(db.Integer, primary_key=True)   # Primary key column
    name = db.Column(db.String(length=35), nullable=False, unique=True)   # Name column
    price = db.Column(db.Float, nullable=False)   # Price column
    barcode = db.Column(db.String(length=12), unique=True, nullable=False)   # Barcode column
    description = db.Column(db.String(length=1024), nullable=False, unique=True)   # Description column
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key column referencing the User model's primary key

    def __repr__(self):   # Define a string representation for the Item model
        return f"Item {self.name}"
    
    def buy(self, user):   # Define a method to handle the purchase of an item by a user
        self.owner = user.id  # Update the owner of the item to the user's ID
        user.budget -= self.price  # Deduct the price of the item from the user's budget
        db.session.commit()  # Commit the changes to the database

    def sell(self, user):   # Define a method to handle the sale of an item by a user
        self.owner = None  # Update the owner of the sold item to None (indicating that it is no longer owned by any user)
        user.budget += self.price  # Add the price of the sold item to the user's budget
        db.session.commit()  # Commit the changes to the database

# ------------------------------------------------------------------------------
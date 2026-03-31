# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Import necessary modules and components
from gadget_market import app, db  # Import the Flask application instance and the database instance from the gadget_market package

from gadget_market.models import Item, User  # Import the Item, User model from the gadget_market package
from gadget_market.forms import RegisterForm, LoginForm  # Import the forms from the gadget_market package 
from gadget_market.forms import PurchaseItemForm, SellItemForm  # Import the purchase and sell item forms from the gadget_market package

from flask import render_template, redirect, url_for, request  # Import the render_template, redirect, url_for, and request functions for rendering HTML templates and handling redirects
from flask import flash  # Import the flash function for displaying flash messages to users

from flask_login import login_user, logout_user  # Import the login_user and logout_user functions from the flask_login module for handling user login and logout
from flask_login import login_required  # Import the login_required decorator from the flask_login module to protect routes that require user authentication
from flask_login import current_user  # Import the current_user proxy from the flask_login module to access the currently logged-in user in route handlers

# ------------------------------------------------------------------------------
# Home page route
@app.route("/")     # Define the route for the root URL
@app.route("/home")     # Define another route for the /home URL
def home_page():      # Define the function to be executed when the root URL is accessed
    return render_template("home_page.html")       # Render and return the 'home.html' template

# ------------------------------------------------------------------------------
# Market page route
@app.route('/market', methods=['GET', 'POST'])     # Define the route for the /market URL and specify that it can handle both GET and POST requests
@login_required  # Apply the login_required decorator to protect the market page route, ensuring that only authenticated users can access it
def market_page():      # Define the function to be executed when the /market URL is accessed
    # Purchase and Sell Item Forms
    purchaseForm = PurchaseItemForm()  # Create an instance of the PurchaseItemForm class to represent the purchase item form
    sellForm = SellItemForm()  # Create an instance of the SellItemForm class to represent the sell item form

    if (request.method == 'POST'): # Check if the request method is POST, indicating that a form has been submitted
        # Handle purchase item logic
        purchased_item_name = request.form.get('purchased_item')  # Get the value of the 'purchased_item' field from the submitted form data
        purchased_item = Item.query.filter_by(name=purchased_item_name).first()  # Query the database to find the item with the given name
        if purchased_item:  # If the item is found in the database
            # Check User's budget
            if current_user.can_purchase(purchased_item):  # Check if the current user has enough budget to purchase the item using the can_purchase method defined in the User model
                purchased_item.buy(current_user)  # Call the buy method on the purchased item, passing the current user as an argument to handle the purchase logic (e.g., updating ownership, deducting budget, etc.)
                flash(f"You have purchased {purchased_item.name} for £{purchased_item.price}!", category='success')  # Flash a success message to be displayed to the user after successful purchase
            else:
                flash(f"Unfortunately, you don't have enough budget to purchase {purchased_item.name}!", category='danger')  # Flash an error message to be displayed to the user if they don't have enough budget to purchase the item
                
        # Handle sell item logic
        sell_item_name = request.form.get('sold_item')  # Get the value of the 'sold_item' field from the submitted form data
        sold_item = Item.query.filter_by(name=sell_item_name).first()  # Query the database to find the item with the given name
        if sold_item:  # If the item is found in the database
            if current_user.can_sell(sold_item):  # Check if the current user can sell the item using the can_sell method defined in the User model
                sold_item.sell(current_user)  # Call the sell method on the sold item, passing the current user as an argument to handle the sale logic (e.g., updating ownership, adding budget, etc.)
                flash(f"You have sold {sold_item.name} for £{sold_item.price}!", category='success')  # Flash a success message to be displayed to the user after successful sale
            else:
                flash(f"Unfortunately, you don't have {sold_item.name} in your inventory to sell!", category='danger')  # Flash an error message to be displayed to the user if they don't have the item in their inventory to sell

        # Redirect back to the market page after handling the purchase
        return redirect(url_for('market_page'))

    # Get items from the database to display on the market page
    if request.method == 'GET':  # Check if the request method is GET, indicating that the market page is being accessed for the first time or refreshed
        # items = Item.query.all()  # Retrieve all items from the database
        items = Item.query.filter_by(owner=None)    # Retrieve all items without 'owner' from the database

        # Current user's items
        owned_items = Item.query.filter_by(owner=current_user.id)  # Retrieve all items owned by the current user from the database

        return render_template("gadget_market_page.html", items=items, purchaseForm=purchaseForm, owned_items=owned_items, sellForm=sellForm)
        # Render and return the 'market.html' template

# ------------------------------------------------------------------------------
# Register page route
@app.route('/register', methods=['GET', 'POST'])     # Define the route for the /register URL and specify that it can handle both GET and POST requests
def register_page():    # Define the function to be executed when the /register URL is accessed
    form = RegisterForm()   # Create an instance of the RegisterForm class to represent the registration form

    if form.validate_on_submit():  # Check if the form is submitted and valid
        new_user = User(username=form.username.data, email=form.email.data, password_hash=form.password1.data)  # Create a new User instance with the form data
        
        # Save the new user to the database (e.g., using SQLAlchemy)
        db.session.add(new_user)  # Add the new user to the database session
        db.session.commit()   # Commit the session to save the new user to the database

        # Log in the new user after successful registration
        login_user(new_user)  # Log in the new user after successful registration
        flash(f"Account created successfully! You are now logged in as {new_user.username}.", category='success')  # Flash a success message to be displayed to the user after successful registration

        # Redirect to a different page after successful registration (e.g., home page, login page, etc.)
        return redirect(url_for('market_page'))  # Redirect to the market page after successful
    
    if form.errors != {}:    # This will return a dictionary of field names and their corresponding error messages if there are validation errors in the form. If there are no errors, it will return an empty dictionary.
        for err_msg in form.errors.values():  # Iterate through the error messages in the form errors
            flash(f"There was an error with creating a user: {err_msg}", category='danger')  # Flash the error message to be displayed to the user (e.g., using Flask's flash function)

    return render_template("registration_page.html", form=form)     # Render and return the 'register.html' template, passing the form instance to the template for rendering the form fields

# ------------------------------------------------------------------------------
# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Create an instance of the LoginForm class to represent the login form
    form = LoginForm()

    # Logic to handle login form submission and user authentication
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()  # Query the database to find a user with the given username
        if attempted_user:
            if attempted_user.check_password(form.password.data):  # Check if the user exists and the password is correct using the check_password method defined in the User model
                login_user(attempted_user)
                flash(f"Login successful! Welcome, {attempted_user.username}!", category='success')  # Flash a success message to be displayed to the user after successful login
                return redirect(url_for('market_page'))  # Redirect to the market page after successful login
            else:
                flash(f"Invalid Password, Please try again.", category='danger')  # Flash the error message to be displayed to the user (e.g., using Flask's flash function)
            
        else:
            flash(f"Invalid Username, Please try again.", category='danger')  # Flash the error message to be displayed to the user (e.g., using Flask's flash function)
        
    return render_template("login_page.html", form=form)

# ------------------------------------------------------------------------------
@app.route('/logout')
def logout_page():
    logout_user()  # Log out the user and clear their session
    flash("You have been logged out!", category='info')  # Flash a message to be displayed to the user after logging out
    return redirect(url_for('home_page'))  # Redirect to the home page after logging out

# ------------------------------------------------------------------------------

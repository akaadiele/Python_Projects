
# ------------------------------------------------------------------------------
# Run the Flask Application

# Importing Modules
from gadget_market import app    # Import the Flask application instance from the gadget_market package

# ------------------------------------------------------------------------------
# Check if the run.py file is being executed directly and not imported as a module
if __name__ == '__main__':  # Check if the script is being run directly (as the main program)
    app.run(debug=True)  # Start the Flask development server with debug mode enabled

# ------------------------------------------------------------------------------
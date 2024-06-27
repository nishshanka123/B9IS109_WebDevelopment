Web Development Project

components to install
python 3.6
flask and its addons
mysql

Start the flask applciation on the disired IP and the port.
flask --app flaskr run --debug --host=0.0.0.0 --port=8080


references:
https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-callproc.html


To address the warning about the SameSite attribute for cookies, you can configure Flask to set the SameSite attribute for the session cookie. The SameSite attribute helps prevent Cross-Site Request Forgery (CSRF) attacks by controlling when cookies are sent.

Here’s how you can configure it in your Flask application:

Step 1: Update Flask Configuration
In your create_app function, you can add configurations to set the SameSite attribute for the session cookie. You may also want to set the Secure attribute to ensure the cookie is only sent over HTTPS connections.

python
Copy code
from flask import Flask, session, redirect, url_for, request, render_template, g, jsonify
from flaskr.config import Config
from flaskr.db import Database
from flaskr.authenticate import authenticate_bp

# application factory
def create_app():
    app = Flask(__name__)
    app.secret_key = 'AAABBBCCCDDD'
    app.config.from_object(Config)

    # Configure session cookie settings
    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",  # Set SameSite attribute (None, Lax, or Strict)
        SESSION_COOKIE_SECURE=True  # Ensure cookies are only sent over HTTPS
    )

    # create the db config
    db_config = {
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'host': app.config['MYSQL_HOST'],
        'database': app.config['MYSQL_DB']
    }

    # pre-initiate the app, setup the database connection and make it available for global context
    @app.before_request
    def before_request():
        if 'db' not in g:
            g.db = Database(db_config)
            g.db.connect()

    # disconnect the database at app teardown
    @app.teardown_appcontext
    def close_db_connection(exception):
        db = g.pop('db', None)
        if db is not None:
            db.disconnect()
    
    # do register the authentication blueprint
    app.register_blueprint(authenticate_bp)

    ###########################################
    ##  route to website index and other pages.
    ###########################################
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')
    
    ## Task Dashboard
    @app.route('/dashboard',methods=['GET', 'POST'])
    def loadDashboard():            
        if 'user_name' in session:
            return render_template('dashboard.html')
        else:
            return redirect(url_for("index"))
        
    ## About Us
    @app.route('/about',methods=['GET', 'POST'])
    def about():   
        response = {
            'message': 'User registration failed',            
        }         
        return render_template('about.html', data="Kawuda yako mee pittu hadanne....?")

        
    ## Contact Us
    @app.route('/contact',methods=['GET', 'POST'])
    def contact():            
        return render_template('contact.html')
        
    return app

# Run application as a python file
Step 2: Ensure HTTPS in Development (Optional)
If you are developing locally and want to test with HTTPS, you can use tools like flask-talisman to enforce HTTPS and set secure headers.

bash
Copy code
pip install flask-talisman
Then, update your create_app function to use Talisman:

python
Copy code
from flask_talisman import Talisman

def create_app():
    app = Flask(__name__)
    app.secret_key = 'AAABBBCCCDDD'
    app.config.from_object(Config)

    # Configure session cookie settings
    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",  # Set SameSite attribute (None, Lax, or Strict)
        SESSION_COOKIE_SECURE=True  # Ensure cookies are only sent over HTTPS
    )

    Talisman(app)  # Enforce HTTPS and set secure headers

    # ... rest of the code
Step 3: Testing and Deployment
Ensure that your app is running over HTTPS in your production environment.
Test the behavior in different browsers to make sure that the SameSite attribute is correctly applied.
Summary
By configuring the SESSION_COOKIE_SAMESITE and SESSION_COOKIE_SECURE settings in Flask, you can ensure that your cookies are sent with the appropriate attributes to enhance security and comply with modern browser requirements.
from flask import Flask, session, redirect, url_for, request, render_template, g
from flaskr.config import Config
from flaskr.db import Database
from flaskr.authenticate import authenticate_bp

# application factory
def create_app():
    app = Flask(__name__)
    app.secret_key = 'AAABBBCCCDDD'
    app.config.from_object(Config)

    # create the db config
    db_config = {
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'host': app.config['MYSQL_HOST'],
        'database': app.config['MYSQL_DB']
    }

    # pre-initiate the app, setup the database connection and make it available for globel context
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
        if session['user_name']:
            return render_template('dashboard.html')
        else:
            return redirect(url_for("index"))
        
    ## About Us
    @app.route('/about',methods=['GET', 'POST'])
    def about():            
        return render_template('about.html')

        
    ## Contact Us
    @app.route('/contact',methods=['GET', 'POST'])
    def contact():            
        return render_template('contact.html')
        

    return app

# Run application as a python file
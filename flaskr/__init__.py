from flask import Flask, render_template 
from flaskr.config import Config
from flaskr.db import Database
from flaskr.authenticate import authenticate_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # create the db config using the Config object
    db_config = {
        'user' : app.config['MYSQL_USER'],
        'password' : app.config['MYSQL_PASSWORD'],
        'host' : app.config['MYSQL_HOST'],
        'database' : app.config['MYSQL_DB']
    }

    #create DB object and connect with the database
    db = Database(db_config)
    db.connect()

    # add the db to the app config
    app.config['db'] = db

    #register the authenticate blueprint
    app.register_blueprint(authenticate_bp)

    ###########################################
    ##  route to website index
    ###########################################
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.teardown_appcontext
    def close_db_connection(exception):
        db.disconnect()

    return app
import os
from flask import Flask, render_template

# Flask application factory create_app()
def create_app(app_config=None):
    # create and configure the app
    # create a flask instance
    app = Flask(__name__, instance_relative_config=True)

    # SECRET_KEY is used by Flask and extensions to keep data safe. 
    # It’s set to 'dev' to provide a convenient value during development, but it should be 
    # overridden with a random value when deploying.
    app.config.from_mapping(
        SECRET_KEY='dev',        
    )

    # implement loading the application configuration from an external file
    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(app_config)

    # route to website index
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    #initialize the database connectivity
    
    return app

    app = Flask(__name__)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
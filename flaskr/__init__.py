from flask import Flask, session, redirect, url_for, request, render_template, g, jsonify
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
            select_query = None
            if session['role_id'] == 1:
                select_query = "Select ptask_id, task_name, task_type, points, description from ptc_publisher_task where user_name = %"
            elif session['role_id'] == 2:
                select_query = "Select ptask_id, task_name, task_type, points from ptc_publisher_task where user_name = %"
            else:
                select_query = "Select ptask_id, task_name, task_type, points from ptc_publisher_task where user_name = %"

            result = fetch_query(select_query, session['user_name']);

            return render_template('dashboard.html')
        else:
            return redirect(url_for("index"))
        
    ## Publish a task
    @app.route('/publishTask',methods=['GET', 'POST'])
    def publishTask():            
        if session['user_name']:
            if request.method == 'POST':
                # Extract job type
                job_type = request.form.get('type_list')
                
                # Extract number of fields
                no_of_fields = int(request.form.get('no_of_fields'))
                
                # Extract dynamically generated fields
                form_data = {}
                for i in range(1, no_of_fields + 1):
                    field_value = request.form.get(f'field_{i}')
                    data_type = request.form.get(f'data_type_{i}')
                    form_data[f'field_{i}'] = {'value': field_value, 'data_type': data_type}

                # Print form data (for debugging)
                print(f"Job Type: {job_type}")
                print(f"Number of Fields: {no_of_fields}")
                for key, value in form_data.items():
                    print(f"{key}: {value}")

                response = {
                            'message': 'Task successfully Created.',
                            'data': {
                                'message': f'Task successfully Created.',
                                'status': "success",
                            }
                        }
                
                return jsonify(response)
            else:
                pass
            print("test------------> end")
            return render_template('publish_task.html')
        else:
            return redirect(url_for("index"))
        
    
    ## Update task
    @app.route('/updateTask',methods=['GET', 'POST'])
    def updateTask():            
        if session['user_name']:
            return render_template('publish_task.html')
        else:
            return redirect(url_for("index"))
        

    ## Update task
    #@app.route('/updateTask',methods=['GET', 'POST'])
    #def updateTask():            
    #    if session['user_name']:
    #        return render_template('update_task.html')
    #    else:
    #        return redirect(url_for("index"))
        
    ## About Us
    @app.route('/about',methods=['GET', 'POST'])
    def about():   
        response = {
            'message': 'User registered failed',            
            }         
        return render_template('about.html', data="Kawuda yako mee pittu hadanne....?")

        
    ## Contact Us
    @app.route('/contact',methods=['GET', 'POST'])
    def contact():            
        return render_template('contact.html')
        

    return app

# Run application as a python file
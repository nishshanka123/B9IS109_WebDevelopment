from flask import Flask, json, session, redirect, url_for, request, render_template, g, jsonify
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
            g.db = Database(db_config['database'])
            g.db.connect()

    # disconnect the database at app teardown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        g.db.close_db(exception)
    
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
            response = None
            db = g.get('db')

            if db is None:
                print("Database connection is None")
                error = "Database connection issue."

            if session['role_id'] == 1:
                select_query = "Select ptask_id, task_name, task_type, points, description from ptc_publisher_task where user_name = ?"
                result = db.fetch_query(select_query, (session['user_name'],))
            elif session['role_id'] == 2:
                select_query = "Select ptask_id, task_name, task_type, points, description from ptc_publisher_task"
                result = db.fetch_query(select_query)
            else:
                pass

            #db = g.get('db')
            #if db is None:
            #    print("Database connection is None")
            #    error = "Database connection issue."
            #else:
            #    print(F"query : {select_query}")
                #result = db.fetch_query(select_query, (session['user_name'],))                
                #db.fetch_query(query, (user_name,))
            
            data = None
            json_data = []
            if result:
                print(f"Results: {result[0]}")
                for result_ob in result:
                    form_data_json = {
                        "title": F"{result_ob['task_name']}",
                        "task_name": F"{result_ob['task_name']}",
                        "description": F"{result_ob['description']}",
                        "task_type" : F"{result_ob['task_type']}",
                        "points" : F"{result_ob['points']}",
                        "task_id" : F"{result_ob['ptask_id']}"
                    }
                    json_data.append(form_data_json)

                '''form_data_json = {
                    "description": "des1",
                    "task_name": "name1",
                    "title": "title1"
                }
                json_data.append(form_data_json)
                form_data_json = {
                    "description": "des2",
                    "task_name": "name2",
                    "title": "title2"
                }
                json_data.append(form_data_json)'''
                
            else:                
                form_data_json = {
                    "description": "There are no available tasks at the moment. Please check later.",
                    "task_name": "No Tasks",
                    "title": "Awaiting for tasks"
                }
                json_data.append(form_data_json)                
                
            data = {'json_data': json_data, 'count': 1}
            return render_template('dashboard.html', form_data=data)
        else:
            return redirect(url_for("index"))
        
    ## Publish a task
    @app.route('/publishTask',methods=['GET', 'POST'])
    def publishTask():            
        if session['user_name']:
            if request.method == 'POST':
                # Extract job details 
                job_type = request.form.get('type_list')
                task_name = request.form.get('task_name')
                desc = request.form.get('desc')
                points = request.form.get('points')
                no_of_slots = request.form.get('no_of_slots')                
                no_of_fields = int(request.form.get('no_of_fields'))                    
                
                # Extract dynamically generated fields
                form_data = {}
                for i in range(1, no_of_fields + 1):
                    field_value = request.form.get(f'field_{i}')
                    data_type = request.form.get(f'data_type_{i}')
                    form_data[f'field_{i}'] = {'value': field_value, 'data_type': data_type}

                # Print form data (for debugging)
                form_data_json = json.dumps({
                    "job_type": job_type,
                    "no_of_fields": no_of_fields,
                    "fields": form_data
                }, indent=4)
                print(form_data_json)

                # Print form data (for debugging)
                print(f"Job Type: {job_type}")
                print(f"Number of Fields: {no_of_fields}")
                for key, value in form_data.items():
                    print(f"{key}: {value}")

                data_in_text = "insert into ptc_publisher_task (user_name, task_name, number_of_slots, task_type, points, description, task_data) values (?,?,?,?,?,?,?)"
                
                db = g.get('db')
                if db is None:
                    print("Database connection is None")
                    error = "Database connection issue."
                else:
                    result = db.execute_query(data_in_text, (session['user_name'], task_name, no_of_slots, job_type, points, desc, form_data_json,))

                if result:
                    response = {
                                'message': 'Task successfully Created.',
                                'data': {
                                    'message': f'Task successfully Created.',
                                    'status': "success",
                                }
                            }
                else:
                    response = {
                                'message': 'Failed to create the task.',
                                'data': {
                                    'message': f'Failed to create the task.',
                                    'status': "fail",
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
        db = g.get('db')
        if db is None:
            print("Database connection is None")
            error = "Database connection issue."
            
        if session['user_name']:
            return render_template('publish_task.html')
        else:
            return redirect(url_for("index"))
        

    ## Complete Task
    @app.route('/completeTask',methods=['GET', 'POST'])
    def completeTask():
        result = None

        db = g.get('db')
        if db is None:
            print("Database connection is None")
            error = "Database connection issue."

        if session['user_name']:
            if request.method == 'POST':
                task_id = request.form.get('task_id')
                print(F"Received task ID: {task_id}")
                if session['role_id'] == 2:
                    select_query = "Select task_name, description, task_data from ptc_publisher_task where ptask_id = ?"
                    result = db.fetch_query(select_query, (task_id,))
                    
                    if result:
                        task_data = result[0];
                        #print(F"TASK data: {task_data}")

                    jason_task_data = {'task_id':task_id, 'data':task_data}
                    print(F"Json data: {jason_task_data}")
                    return render_template('completeTask.html', data=jason_task_data)
                else:
                    return render_template('completeTask.html')            
        else:
            return redirect(url_for("index"))
        
    ## Execute Task
    @app.route('/executeTask',methods=['GET', 'POST'])
    def executeTask():
        result = None

        if session['user_name']:
            if request.method == 'POST':
                form_data = request.form.to_dict()
                task_id = request.form.get('task_id')
                task_data_json = json.dumps(form_data)
                points = 0
                task_name = "test"
                response = None
                error = None

                db = g.get('db')
                if db is None:
                    print("Database connection is None")
                    error = "Database connection issue."
                else:
                    query = "insert into ptc_client_task(ptask_id, task_name, points, data) values (?, ?, ?, ?)"
                    result = db.execute_query(query, (task_id, task_name, points, task_data_json,))
                    if result:
                        response = {
                                'message': 'Well done. Task completed, Thank you for your time.',
                                'data': {
                                    'message': f'Task completed successfully',
                                    'status': "success",
                                }
                            }
                    else:
                        error = "Internal server error"
                
                if error is not None:
                    response = {
                                'message': 'We are sorry, Unable to complete the task, Thank you for your time.',
                                'data': {
                                    'message': error,
                                    'status': "fail",
                                }
                            }
                return jsonify(response)
            else:
                return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
        

        
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


app = create_app()

# Run application as a python file
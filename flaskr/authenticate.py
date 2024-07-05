
from flask import (
    Blueprint, 
    render_template,
    request,
    redirect,
    url_for,
    flash,
    g,
    session,
    jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

#from app.models import User

authenticate_bp = Blueprint('authenticate', __name__, url_prefix='/auth')
bcrypt = Bcrypt()

@authenticate_bp.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    error = None
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        password_c = request.form['confirm_password']
        security_q = request.form['sec_qlist']
        security_qa = request.form['sec_qa']
        terms_accepted = 'terms' in request.form
        pub_or_sub = 'pub_or_sub' in request.form

        print("pub or sub: " , pub_or_sub)
        if pub_or_sub:
            pub_or_sub = 1
        else:
            pub_or_sub = 2

        if not user_name:
            error = 'User name should not be empty'
        elif not password:
            error = 'Password should not be empty'
        elif not terms_accepted:
            error = 'Terms and Conditions are not accepted.'
        elif password != password_c:
            error = 'Passwords do not match.'

        if error is None:
            db = g.get('db')
            if db is None:
                print("DB connection is None")
                error = "Database connection issue."

            try:
                insert_q = '''INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id) 
                              VALUES (?, ?, ?, ?, ?, ?)'''
                insert_user_info = '''INSERT INTO user_info(user_name, email, first_name, last_name, date_of_birth, address_line1, address_line2, area_code) 
                                VALUES(?,?,?,?,?,?,?,?)'''
                #hashed_password = generate_password_hash(password)
                #print(F"query: {insert_q}")
                
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                #db.execute_query(insert_q, (user_name, email, hashed_password, security_q, security_qa, '1'))
                #result_message = db.call_register_user(user_name, email, hashed_password, security_q, security_qa, pub_or_sub)
                result = db.execute_query(insert_q, (user_name, email, hashed_password, security_q, security_qa, pub_or_sub,))
                print(F"test---->: {result}")
                if result >= 0:
                    result2 = db.execute_query(insert_user_info, (user_name, email, '', '', '', '', '', '',))
                    response = {
                                'message': "User registration successful",
                                'data': {
                                    'message': "User registration successful",
                                    'status': "success",
                                    'redirect_url': url_for('authenticate.login')
                                }
                            }
                    return jsonify(response)
                    #return redirect(url_for("authenticate.login"))
                else:
                    #print(f"test----> {result}")
                    response = {
                                'message': result,
                                'data': {
                                    'message': result,
                                    'status': "fail"
                                }
                            }
                    return jsonify(response)
                    

            except Exception as ex:
                print(f"Database error occurred: {ex}")
                error = F"Registration failed : {ex}"
                response = {
                                'message': 'Registration failed: Database server error',
                                'data': {
                                    'message': error,
                                    'status': "fail"
                                }
                            }
                return jsonify(response)
            else:
                flash('Your account has been created! You can now log in.', 'success')
                return redirect(url_for("authenticate.login"))
        else:
            #response = {'message': 'Error: ', 'data': 'Error'}
            error = F"User registration failed : {error}"
            response = {
                            'message': error,
                            'data': {
                                'message': error,
                                'status': "fail"
                            }
                        }
            return jsonify(response)
    
    return render_template('auth/registerUser.html')

@authenticate_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        if not user_name or not password:
            error = "Login failed: User name or password is empty. Please check and retry."
            print("user name or password is empty")
        else:
            db = g.get('db')
            if db is None:
                print("Database connection is None")
                error = "Database connection issue."
            else:
                user_data = None
                print("Get the user information from db")
                try:
                    query = "SELECT * FROM auth_info WHERE user_name=?"
                    user_data = db.fetch_query(query, (user_name,))
                    print(f"user data---> {user_data}")
                except Exception as ex:
                    print(f"DB query execution error occurred: {ex}")
                    error = "Database query error."

                if user_data:
                    print("user data: ", user_data)
                    user_data = user_data[0]
                    hpwd = bcrypt.generate_password_hash(password).decode('utf-8')
                    #if not check_password_hash(user_data['pwd_hash'], password):
                    #print(F"pwds : {user_data[0]} : {hpwd}")

                    if user_data:
                        #print(F"user_data: {user_data['pwd_hash']}")
                        if not bcrypt.check_password_hash(user_data['pwd_hash'], password):
                            error = "Incorrect credentials. Please check your login and try again."
                    else:
                        error = "Incorrect credentials. Please check your login and try again."
                else:
                    error = "Incorrect credentials. Please check your login and try again."

        if error is None:
            session.clear()
            session['user_name'] = user_data['user_name']
            session['role_id'] = user_data['role_id']
            response = {
                            'message': 'success',
                            'data': {
                                'message': 'success',
                                'status': "success",
                                'redirect_url': url_for('index')
                            }
                        }
            #return redirect(url_for("index"))
            return jsonify(response)
        else:
            print("TEST---> 1")
            response = {
                            'message': 'Authentication failure',
                            'data': {
                                'message': f'Authentication failure, {error}',
                                'status': "fail",
                            }
                        }
            flash(error)
            return jsonify(response)
    else:
        pass

    return render_template('auth/login.html')

# Logout API
@authenticate_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if session['user_name']:
        print("clearing session and signing out")
        session.clear()
        return redirect(url_for("index"))
    else:
        print("No active user signed in")
        
    return render_template('auth/login.html')


@authenticate_bp.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    error = None
    if request.method == 'POST':
        pass
    else:
        if session['user_name']:
            select_query = None
            response = None
            db = g.get('db')
            result = None
            if db is None:
                print("Database connection is None")
                error = "Database connection issue."
            else:
                select_query = "Select * from user_info where user_name = ?"
                result = db.fetch_query(select_query, (session['user_name'],))
                print(f"TEST-------> {result}")
                
                data = None
                json_data = []
                if result:
                    print(f"Results: {result[0]}")
                    for result_ob in result:
                        form_data_json = {
                            "user_name": F"{result_ob['user_name']}",
                            "email": F"{result_ob['email']}",
                            "first_name": F"{result_ob['first_name']}",
                            "last_name" : F"{result_ob['last_name']}",
                            "date_of_birth" : F"{result_ob['date_of_birth']}",
                            "address_line1" : F"{result_ob['address_line1']}",
                            "address_line2" : F"{result_ob['address_line2']}",
                            "area_code" : F"{result_ob['area_code']}"
                        }
                        json_data.append(form_data_json)                
                else:
                    print("TEST--------> No data")
                    form_data_json = {
                        "description": "There are no available tasks at the moment. Please check later.",
                        "task_name": "No Tasks",
                        "title": "Awaiting for tasks"
                    }
                    json_data.append(form_data_json)                
                    
                data = {'json_data': json_data, 'count': 1}
                return render_template('auth/updateProfile.html', form_data=data)
        else:
            return redirect(url_for("index"))


@authenticate_bp.route('/viewProfile', methods=['GET', 'POST'])
def viewProfile():
    error = None
    if request.method == 'POST':
        pass
    else:
        if session['user_name']:
            select_query = None
            response = None
            db = g.get('db')
            result = None
            if db is None:
                print("Database connection is None")
                error = "Database connection issue."
            else:
                select_query = "Select * from user_info where user_name = ?"
                result = db.fetch_query(select_query, (session['user_name'],))
                
                data = None
                json_data = []
                if result:
                    print(f"Results: {result[0]}")
                    for result_ob in result:
                        form_data_json = {
                            "user_name": F"{result_ob['user_name']}",
                            "email": F"{result_ob['email']}",
                            "first_name": F"{result_ob['first_name']}",
                            "last_name" : F"{result_ob['last_name']}",
                            "date_of_birth" : F"{result_ob['date_of_birth']}",
                            "address_line1" : F"{result_ob['address_line1']}",
                            "address_line2" : F"{result_ob['address_line2']}",
                            "area_code" : F"{result_ob['area_code']}"
                        }
                        json_data.append(form_data_json)                
                else:
                    form_data_json = {
                        "description": "There are no available tasks at the moment. Please check later.",
                        "task_name": "No Tasks",
                        "title": "Awaiting for tasks"
                    }
                    json_data.append(form_data_json)                
                    
                data = {'json_data': json_data, 'count': 1}
                return render_template('auth/viewProfile.html', form_data=data)
        else:
            return redirect(url_for("index"))
     

# My earnings
@authenticate_bp.route('/myEarning', methods=['GET', 'POST'])
def myEarning():
           
    return render_template('auth/my_earning.html')

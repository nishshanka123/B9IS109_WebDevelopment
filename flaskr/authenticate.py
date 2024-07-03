
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
                #insert_q = '''INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id) 
                #              VALUES (%s, %s, %s, %s, %s, %s)'''
                #hashed_password = generate_password_hash(password)
                #print(F"query: {insert_q}")
                
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                #db.execute_query(insert_q, (user_name, email, hashed_password, security_q, security_qa, '1'))
                result_message = db.call_register_user(user_name, email, hashed_password, security_q, security_qa, pub_or_sub)
                print(F"test----1: {result_message}")
                if result_message == 'SUCCESS':
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
                    #print(f"test----> {result_message}")
                    response = {
                                'message': result_message,
                                'data': {
                                    'message': result_message,
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
                except Exception as ex:
                    print(f"DB query execution error occurred: {ex}")
                    error = "Database query error."

                if user_data:
                    #print("user data: ", user_data)
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


@authenticate_bp.route('/updateUser', methods=['GET', 'POST'])
def updateUser():
    error = None
    if request.method == 'POST':
        user_name = request.form['name']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address_line1 = request.form['address_line1']
        address_line2 = request.form['address_line2']
        area_code = request.form['area_code']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        country = request.form['country']

        if not user_name:
            error = 'User name should not be empty'
        elif not password:
            error = 'Password should not be empty'

        if error is None:
            db = g.get('db')
            try:
                update_q = """UPDATE user_info SET email=%s, first_name=%s, last_name=%s, date_of_birth=%s, address_line1=%s, 
                              address_line2=%s, area_code=%s WHERE user_name=%s"""
                db.execute_query(update_q, (email, first_name, last_name, user_name, address_line1, address_line2, area_code))
            except Exception as ex:
                print(f"Database error occurred: {ex}")
                flash(f"Error: {str(ex)}", 'danger')
            else:
                return redirect(url_for("auth.login"))
        flash(error, 'danger')
    return render_template('auth/registerUser.html')


# My earnings
@authenticate_bp.route('/myEarning', methods=['GET', 'POST'])
def myEarning():
           
    return render_template('auth/my_earning.html')

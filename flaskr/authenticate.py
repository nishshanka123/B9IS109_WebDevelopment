from flask import (
    Blueprint, 
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)
from werkzeug.security import generate_password_hash, check_password_hash

authenticate_bp = Blueprint('authenticate', __name__, url_prefix='/auth')

@authenticate_bp.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    user_name = None
    email = None
    password = None
    password_c = None
    security_q = None
    security_qa = None    

    confirm_password = None
    country = None
    terms_accepted = False
    error = None
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        password_c = request.form['confirm_password']
        security_q = request.form['sec_qlist']
        security_qa = request.form ['sec_qa']
        terms_accepted = 'terms' in request.form

        if not user_name:
            error = 'User name should not empty'
        elif not password:
            error = 'Password should not empty'
        
        print(f"Auth: {terms_accepted}")
        if not terms_accepted:
            error = 'Terms and Conditions are not accepted.'


        if error is None:
            #get the db from current application
            db = current_app.config['db']
            if db is None:
                print("DB connection is None")

            try:
                insert_q = '''INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id) values (%s, %s, %s, %s, %s, %s)'''
                #print(f"insert_q",(user_name, email, password, security_q, security_qa, 1) )
                #insert_q = "INSERT INTO user_info (email, first_name, last_name, user_name, date_of_birth, address_line1, address_line2, area_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                #db.execute_query("INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id) values (%s, %s, %s, %s, %s, %s)", (user_name, email, password, security_q, security_qa, '1') )
                db.execute_query(insert_q, (user_name, email, password, security_q, security_qa, '1') )

            except Exception as ex:
                #flash(f"Error: {str(ex)}", 'danger')
                print(f"Database error occurred: {ex}")
            else:
                return redirect(url_for("authenticate.login"))
        else:
            print(f"Form submission error: {error}")
            flash(error, 'danger')
            return redirect(url_for('authenticate.registerUser') )
    elif request.method == 'GET':
        pass


    return render_template('auth/registerUser.html')

@authenticate_bp.route('/updateUser', methods=['GET', 'POST'])
def updateUser():
    print("updateUser: ------------> 1")
    print("request.form: " , request.form)
    user_name = None
    email = None
    password = None
    first_name = None
    last_name = None
    address_line1 = None
    address_line2 = None
    date_of_birth = None
    area_code = None

    confirm_password = None
    country = None
    tnc = False
    if request.method == 'POST':
        print("updateUser: ------------> 2")
        name = request.form['name']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address_line1 = request.form['address_line1']
        address_line2 = request.form ['address_line2']
        area_code = request.form['area_code']

        password = request.form['password']
        confirm_password = request.form['confirm_password']
        country = request.form['country']
        #tnc = request.form['terms']
        
        error = None
    if not user_name:
        error = 'User name should not empty'
    elif not password:
        error = 'Password should not empty'

    if error is None:
        #get the db from current application
        db = current_app.config['db']
        try:
            insert_q = "INSERT INTO user_info (email, first_name, last_name, user_name, date_of_birth, address_line1, address_line2, area_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            db.execute_query(insert_q, email, first_name, last_name, user_name, date_of_birth, address_line1, address_line2, area_code)
        except Exception as ex:
            flash(f"Error: {str(ex)}", 'danger')
        else:
            return redirect(url_for("auth.login"))
            

    return render_template('auth/registerUser.html')

@authenticate_bp.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('auth/login.html')


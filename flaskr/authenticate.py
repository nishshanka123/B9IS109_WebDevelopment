
from flask import (
    Blueprint, 
    render_template,
    request,
    redirect,
    url_for,
    flash,
    g,
    session
)
from werkzeug.security import generate_password_hash, check_password_hash

authenticate_bp = Blueprint('authenticate', __name__, url_prefix='/auth')

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

        if not user_name:
            error = 'User name should not be empty'
        elif not password:
            error = 'Password should not be empty'
        elif not terms_accepted:
            error = 'Terms and Conditions are not accepted.'

        if error is None:
            db = g.get('db')
            if db is None:
                print("DB connection is None")

            try:
                insert_q = '''INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id) 
                              VALUES (%s, %s, %s, %s, %s, %s)'''
                hashed_password = generate_password_hash(password)
                db.execute_query(insert_q, (user_name, email, hashed_password, security_q, security_qa, '1'))
            except Exception as ex:
                print(f"Database error occurred: {ex}")
                error = "Registration failed."
            else:
                return redirect(url_for("authenticate.login"))
        flash(error, 'danger')
        return redirect(url_for('authenticate.registerUser'))

    return render_template('auth/registerUser.html')

@authenticate_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        #print("--------------Login: POST request received")

        if not user_name or not password:
            error = "Login failed: User name or password is empty. Please check and retry."
            print("user name or password is empty")
        else:
            db = g.get('db')
            if db is None:
                print("Database connection is None")
                error = "Database connection issue."
            else:
                print("Get the user information from db")
                try:
                    query = "SELECT * FROM auth_info WHERE user_name=%s"
                    user_data = db.fetch_query(query, (user_name,))
                except Exception as ex:
                    print(f"DB query execution error occurred: {ex}")
                    error = "Database query error."

                if user_data:
                    #print("user data: ", user_data)
                    user_data = user_data[0]
                    #if not check_password_hash(user_data['pwd_hash'], password):
                    if password != user_data['pwd_hash']:
                        error = "Incorrect credentials. Please check your login and try again."
                else:
                    error = "Incorrect credentials. Please check your login and try again."

        if error is None:
            session.clear()
            session['user_name'] = user_data['user_name']
            return redirect(url_for("index"))
        flash(error)
    else:
        pass

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

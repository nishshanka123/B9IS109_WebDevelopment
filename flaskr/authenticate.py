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
    print("registerUser: ------------> 1")
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
        print("registerUser: ------------> 2")
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
            

    return render_template('auth/registerUser.html')

@authenticate_bp.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('auth/login.html')


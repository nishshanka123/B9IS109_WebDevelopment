import functools

from flask import(
    Blueprint, 
    flash, 
    g, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# create authentication as view a blueprint
authenticate_bp = Blueprint('authenticate', __name__, url_prefix='/authenticate')

#add a Blueprint route
@authenticate_bp.route('/registerUser', methods=('GET', 'POST'))
def registerUser():
    print("registerUser: ------------> 1")
    username = None
    password = None
    if request.form == 'POST':
        print("registerUser: ------------> 2")
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
    if not username:
        error = 'User name should not empty'
    elif not password:
        error = 'Password should not empty'
    
    if error is None:
        # Execute the DB queries to add a new user
        insertQ = 'INSERT INTO user (username, password) VALUES (?, ?)'
        try:
            db_cursor = db.cursor()
            db_cursor.execute(insertQ, username, password)
        except db_cursor.error as err:
            error = f"DB error occurred: {err}"
        else:
            redirect(url_for(auth.login))
        
        db.commit()
        db_cursor.close()

        flash(error)

    return render_template('auth/registerUser.html')

@authenticate_bp.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')




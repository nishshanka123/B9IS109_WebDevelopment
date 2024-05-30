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

authenticate_bp = Blueprint('authenticate', __name__, url_prefix='/authenticate')
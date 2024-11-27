from flask import Blueprint
from flask_login import current_user

auth=Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'This is the login page'

@auth.route('/sign_up')
def sign_up():
    return 'This is the sign_up page'
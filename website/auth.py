from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm #PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user

auth=Blueprint('auth', __name__)

@auth.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html', form=form)

@auth.route('/sign_up')
def sign_up():
    form=SignUpForm()
    return render_template('signup.html', form=form)
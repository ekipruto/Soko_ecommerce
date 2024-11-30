from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm #PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user

auth=Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form=SignUpForm()

    if form.validate_on_submit(): #this does the automatic validation for both email and password check on characters
        email=form.email.data
        username=form.username.data
        password1=form.password1.data
        password2=form.password2.data

        if password1==password2:
            new_customer=Customer()
            new_customer.email=email
            new_customer.username=username
            new_customer.password=password2

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully, proceed to login')
                return redirect('/login')
            
            except Exception as e:
                print(e)
                flash('Account not created, Email already exists try again')

                form.email.data=''
                form.username.data=''
                form.password1.data-=''
                form.password2.data=''


    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    #getting user inputs
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data

        #checking if customer exists/ remember the email was unique and cannot be the 
        #same for two or more users
        customer=Customer.query.filter_by(email=email).first()

        #if customer exists then check if the password is correct
        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Incorect email and/or password')

        else:
            flash('Account does not exist, please sign up')


    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')
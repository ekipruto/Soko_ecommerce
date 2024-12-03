from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm, PasswordChangeForm
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
    if form.validate_on_submit():  #checking to see if the values submitted by the customer are valid
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

@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):   #customer_id is the integer that will pick or load the specific customer 
                            #whose password to change
    print('Customer Id is:', customer_id)
    #return ('Customer Id is:', customer_id)
    #Queerying the database to get the instatnce of the customer
    customer=Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)

@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):   #customer_id is the integer that will pick or load the specific customer 
                                    #whose password to change
    form = PasswordChangeForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():   #checking to see if the values submitted by the customer are valid
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Password Updated Successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New Passwords do not match!!')

        else:
            flash('Current Password is Incorrect')

    return render_template('change_password.html', form=form)
    
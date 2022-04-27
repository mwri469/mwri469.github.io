from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Create our login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get login info from user, query against database
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', user=current_user)

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get the users details
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        # Check details are valid
        if len(email) == 0:
            flash('Please enter an email', category='error')
        elif '@' and '.' not in email:
            flash('Email is invalid', category='error')
        elif len(first_name) == 0:
            flash('Please enter a name', category='error')
        elif len(password1) == 0 or len(password2) == 0:
            flash('Please enter a password', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            # Add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
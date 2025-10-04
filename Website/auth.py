from flask import Blueprint,request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from .forms import LoginForm, RegistrationForm
from .models import User
from . import db

auth = Blueprint('auth',__name__)

'''
First time ever → User must Signup → entry saved in DB
'''
@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email = form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created successfully!')
        return redirect(url_for('auth.login'))
    #form=form passes form object into template and can access it inside login.html
    return render_template('signup.html', title = 'Sign Up', form=form)
@auth.route('/login',methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!','success')
            return redirect(url_for('views.dashboard'))
        else:
            flash('Please check the email and password','danger')
    return render_template('login.html',title = 'Login', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
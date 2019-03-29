from flask import Flask, render_template, flash, redirect, url_for, request
from wrecktionary import app, bcrypt, db
from wrecktionary.forms import LoginForm, RegistrationForm, UpdateAccountForm
from wrecktionary.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts=[
    {
        'author': 'James Eroy', 
        'title': 'Mast', 
        'date_posted': 'April 20, 2018',
        'content': 'A part of the ship'
    },
    {
        'author': 'some anthropologist', 
        'title': 'Poopdeck', 
        'date_posted': 'April 10, 2018',
        'content': 'the dirtiest part of the ship'
        
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:#if user is logged in, user is redirected to the homepage if they are already log in
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You are now able to log!', 'success')
        return redirect(url_for( 'home' ))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else: 
                flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('account'))
    image_file = url_for("static", filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title="account", image_file = image_file, form = form)
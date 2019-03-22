from flask import Flask
from models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit(): 
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for( 'home' ))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            if form.email.data =='admin@blog.com' and form.password.data =='password':
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else: 
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='login', form=form)
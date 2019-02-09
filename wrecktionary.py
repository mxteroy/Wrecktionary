from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '3fe68ef0176e0ea17ea3db319e2fc9cc'
app.config['SQLAlchemy_DATASE_URI'] = 'sqlite:///site.db'

posts=[
    {
        'author': 'James Eroy', 
        'title': 'Blog Post 1', 
        'date_posted': 'April 20, 2018',
        'content': 'Trump'
    },
    {
        'author': 'someone', 
        'title': 'Blog Post 11', 
        'date_posted': 'April 10, 2018',
        'content': 'Shutdown'
        
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

if __name__ == '__main__': 
    app.run(debug=True)
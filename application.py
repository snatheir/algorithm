from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config['SECRET_KEY'] = 'e1953e4286de87ce049e87e26fc85386'

users = [
    {
        'username' : 'user1'
    },
    {
        'username' : 'user2'
    }
]

algorithmList = [
    {
        'link':'smp',
        'title': 'Stable Marriage/Matching (SMP)',
        'author': 'user1',
        'content': 'Finding a stable matching between two equally sized sets of elements given an ordering of preferences for each element.',
    },
    {
        'link':'roommate',
        'title': 'Stable Roommate Problem',
        'author': 'user2',
        'content': 'Finding a stable matching for an even-sized set',
    },
    {
        'link':'nrmp',
        'title': 'Hospitals/Residents Problem (NRMP)',
        'author': 'user1',
        'content': 'My first posts content',
    }
]

@application.route("/")
@application.route("/index")
@application.route("/home")
def home():
    return render_template('index.html')

@application.route("/algorithms")
def algorithms():
    return render_template('algorithms.html', algorithmList=algorithmList)


@application.route("/about")
def about():
    return render_template('about.html', title='About')

@application.route("/algorithm/smp", methods=['GET', 'POST'])
def smp():
    return render_template('smp.html')

@application.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home')) #redirects user to home after successful validation
    return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data =='admin@blog.com' and form.password.data =='password':
            flash('you have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# @app.route('/user/<username>')
# def profile(username):
#     return render_template('about.html', title='User')



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
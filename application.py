from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config['SECRET_KEY'] = 'e1953e4286de87ce049e87e26fc85386'


@application.route("/")
def home():
    return render_template('index.html')

@application.route("/about")
def about():
    return render_template('about.html', title='About')


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

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
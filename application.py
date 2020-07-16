from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from config import SECRET_KEY
application = Flask(__name__)
application.config['SECRET_KEY'] = SECRET_KEY
from db import user_collection, algorithm_collection

algorithmList = [
    {
        'title': 'Stable Marriage/Matching (SMP)',
        'author': 'user1',
        'content': 'Finding a stable matching between two equally sized sets of elements given an ordering of preferences for each element.',
    },
    {
        'title': 'Stable Roommate Problem',
        'author': 'user2',
        'content': 'Finding a stable matching for an even-sized set',
    },
    {
        'title': 'Hospitals/Residents Problem (NRMP)',
        'author': 'user1',
        'content': 'My first posts content',
    }
]


# @application.route("/users/<username>", methods=['GET', 'POST'])
# def user():
#     if flask.request.method == 'POST':
#         users.insert_one({"username": username})
#     else:
#         return render_template('user.html', title=username)
#     return "{username} has been inserted into the user database!"

# @application.route("/algorithms/<algorithm>", methods=['GET', 'POST'])
# def algorithms():
#     if flask.request.method == 'POST':
#         users.insert_one({"algorithm": algorithm})
#     else:
#         pass
#     return "{algorithm} has been inserted into the algorithm database!"



# @application.route("/algorithm/smp", methods=['GET', 'POST'])
# def smp():
#     return render_template('smp.html')



@application.route("/")
@application.route("/index")
@application.route("/home")
def home():
    return render_template('index.html')

@application.route("/about")
def about():
    return render_template('about.html', title='About')

@application.route("/algorithms")
def algorithms():
    return render_template('algorithms.html', algorithmList=algorithmList)

@application.route("/algorithms/submit")
def submit_algorithm():
    return render_template('about.html', title='About')


#test to insert data to the data base
@application.route("/test")
def test():
    algorithm_collection.insert_many(algorithmList)
    return "Connected to the data base!"

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
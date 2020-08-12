from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from flask_bcrypt import Bcrypt
from config import SECRET_KEY
application = Flask(__name__)
application.config['SECRET_KEY'] = SECRET_KEY

from db import Algorithm, User
from flask_login import current_user, login_required
import os
import secrets
from PIL import Image
from flask_mail import Message
from flask_mail import Mail

from utils import *


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.find_one(int(user_id))


login_manager.init_app(application)
mail = Mail()
bcrypt = Bcrypt()



@app.route('/oauth', methods=['POST'])
def login():
    # Parse auth code
    auth_code = request.json.get('auth_code')
    # exchange for a token
    try:
        #upgrade authorization code into a credentials object
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

################           LOGIN AND REGISTER       #############

@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)
        user_collection.insert_one(user)
        flash(f'Account created for {form.username.data}! You can now log in.','success')
        return redirect(url_for('home')) #redirects user to home after successful validation
    return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.filter(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        email = request.form.get('email')
        password = request.form.get('password')
        user_collection.find_one('email'=email)
        if form.email.data =='snatheir@uwo.ca' and form.password.data =='imnottellingyou':
            flash('you have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

################          ALGORITHMS              #########################################################


@application.route("/algorithms")
def algorithms():
    algorithmList = algorithm_collection.find_many()
    return render_template('algorithms.html', algorithmList=algorithmList)

@application.route("/algorithms/<tag>")
def algorithms_tag(tag):
    algorithmList = algorithm_collection.find_many(tag)
    return render_template('algorithms.html', algorithmList=algorithmList)



@application.route("/algorithms/<string:algorithm_id>")
def algorithms_algorithm(algorithm_id):
    algorithm = Algorithm.find_one(algorithm_id)
    return render_template('algorithm.html', title=algorithm.title, algorithm=algorithm)


@application.route("/algorithms/submit")
@login_required
def submit_algorithm():
    form = AlgorithmForm()
    if form.validate_on_submit():
        algorithm = Algorithm(title = form.title.data, 
                                description = form.description.data, 
                                author=current_user,
                                )
        algorithm_collection.insert_one(algorithm)
        flash('Your algorithm has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('about.html', title='New Algorithm', form=form)

@application.route('/algorithms/<string:algorithm_id>/update')
@login_required
def update_algorithm(algorithm_id):
    algorithm = Algorithm.find_one(algorithm_id)
    if algorithm.author != current_user:
        abort(403)
    form = AlgorithmForm()
    if form.validate_on_submit():
        algorithm.title=form.title.data
        algorithm.description = form.description.data
        algorithm.sample_input = form.sample_input.data
        algorithm.sample_output = form.sample_output.data
        algorithm.tags = form.tags.data
        return redirect(url_for('user_algorithm', user = current_user, algorithm_id=algorithm_id))
    elif request.method == 'GET':
        form.title.data = algorithm.title
        form.content.data = algorithm.description
        form.sample_input.data = algorithm.sample_input
        form.sample_output.data = algorithm.sample_output
        form.tags.data = algorithm.tags
    return render_template('submit_algorithm.html', title='Update Algorithm',
                           form=form, legend='Update Algorithm')

@application.route('/algorithms/<string:algorithm_id>/delete')
@login_required
def delete_algorithm(algorithm_id):
    algorithm = Algorithm.find_one(algorithm_id)
    if algorithm.author != current_user:
        abort(403)
    algorithm_collection.delete(algorithm_id)
    flash('Your algorithm has been deleted!', 'success')
    return redirect(url_for('user_algorithms', user = current_user))


################           USERS            ##################################

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@application.route("/user/<user>/<string:algorithm_id>")
def user_algorithm(user, algorithm_id):
    algorithm_collection.find_many(algorithm)
    return render_template('algorithm.html', algorithm=algorithm, author=author)


@app.route('/user/<user>/algorithms')
def user_algorithms(user):
    return render_template('about.html', title=algorithm)

@users.route("/user/", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.filter(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)









###############          HOME                #####################################

@application.route("/")
@application.route("/index")
@application.route("/home")
def home():
    return render_template('index.html')




@application.route("/about")
def about():
    return render_template('about.html', title='About')







if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
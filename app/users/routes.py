from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import RegistrationForm, UpdateProfileForm, LoginForm, ResetPasswordRequestFrom, PasswordResetFrom
from app.users.utils import sending_reset_email, saving_pic


# params: blueprint name, __name__
users = Blueprint('users', __name__)

# no more using 'app', but now user specific: users

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # firstly, bcrypt process
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        # User creating
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # connecting DB
        db.session.add(user)
        # committing
        db.session.commit()
        db.session.rollback()

        # category: success
        flash(f'Account created for {form.username.data}!! Now you can login', 'success')
        # after creating, user goes to login page (login_plain is func name)
        return redirect(url_for('users.login_plain'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login/plain', methods=['GET', 'POST'])
def login_plain():
    # if logged in, go to
    if current_user.is_authenticated:
        print("what")
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# @users.route('/login/oauth')
# def index():
#     if oauth_google.is_logged_in():
#         user_info = oauth_google.get_user_info()
#         return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info,
#                                                                                                             indent=4) + "</pre>"
#
#     return 'You are not currently logged in.'


# logout & redirect to login plain
@users.route('/logout')
def logout():
    # session 날리기
    logout_user()
    return redirect(url_for('users.login_plain'))

# get: visiting site, post: form submit
@users.route('/account', methods=['GET', 'POST'])
# prohibition going page without login if so returing to the login page login_required
@login_required
def account():
    form = UpdateProfileForm()
    # In the case of formsubmit: validation
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = saving_pic(form.picture.data)
            current_user.image_file = picture_file
        # if form is valid, app should be updated with account info updated
        current_user.username = form.username.data
        current_user.email = form.email.data
        # updating in session as well
        db.session.commit()
        # flash successful updated message for users
        flash('your account has been updated!', 'success')
        # post-get redirect pattern
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # User model : image_file column
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # pass the parameter into the template
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/users/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query \
        .filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/requestpasswordreset", methods=['GET', 'POST'])
def requesting_password_reset():
    # if logged in already, go to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestFrom()
    # form validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sending_reset_email(user)
        flash('Check your email inbox!', 'info')
        return redirect(url_for('users.login_plain'))
    return render_template('request_password_reset.html', title="Reset Password Request", form=form)

# getting token through GET
@users.route("/passwordreset/<string:token>", methods=['GET', 'POST'])
def resetting_password(token):
# if logged in, go to
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # validating method in User in models.py
    user = User.validating_token(token)
    if user is None:
        flash('The token is invalid or expired.', 'warning')
        return redirect(url_for('users.requesting_password_reset'))

    form = PasswordResetFrom()

    if form.validate_on_submit():
        # firstly, bcrypt process
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # resetting password!
        user.password = hashed_password
        # committing
        db.session.commit()
        # category: success
        flash(f'Password updated!! Try login!!', 'success')
        # after creating, user goes to login page (login_plain is func name)
        return redirect(url_for('users.login_plain'))

    return render_template('reset_password.html', title="Reset Password", form=form)



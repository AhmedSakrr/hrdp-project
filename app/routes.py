import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from sqlalchemy import exc
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm
from app import os
# from app import oauth_google
from app.models import User, Post, Strain, Animal, Tissue, Sequencing, Analysis
from flask_login import login_user, current_user, logout_user, login_required

app.config['secret_key'] = '9b7f541fc96486f808ad052d004140e9'
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

# app.register_blueprint(oauth_google.app)


@app.route('/')
@app.route('/home')
def home():
    # retrieving posts from db using the Post model
    # page retrieving from request, page arg name, default val = 1, val constraint = int
    page = request.args.get('page', 1, type=int)
    # legacy -> pagination
    # order: order_by(Post.date_posted.desc())
    postsall = Post.query.all()
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    print(postsall)
    print(type(postsall))
    print(type(posts))
    print(posts.total)
    # print(posts)

    return render_template('home.html', title='home', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/data/hrdp')
def data_hrdp():

    tableset = {}
    columnset = {}

    # strain
    # data list
    strains = Strain.query.all()
    # column list
    strain_columns = Strain.metadata.tables['Strain'].columns.keys()

    tableset['strain'] = strains
    columnset['strain'] = strain_columns

    # animal
    # data list
    animals = Animal.query.all()
    # column list
    animal_columns = Animal.metadata.tables['Animal'].columns.keys()

    tableset['animal'] = animals
    columnset['animal'] = animal_columns

    # tissue
    # data list
    tissues = Tissue.query.all()
    # column list
    tissue_columns = Tissue.metadata.tables['Tissue'].columns.keys()

    tableset['tissue'] = tissues
    columnset['tissue'] = tissue_columns

    # sequencing
    # data list
    sequencings = Sequencing.query.all()
    # column list
    sequencing_columns = Sequencing.metadata.tables['Tissue'].columns.keys()

    tableset['sequencing'] = sequencings
    columnset['sequencing'] = sequencing_columns

    # analysis
    # data list
    analyses = Analysis.query.all()
    # column list
    analysis_columns = Analysis.metadata.tables['Tissue'].columns.keys()

    tableset['analysis'] = analyses
    columnset['analysis'] = analysis_columns

    return render_template('data_hrdp.html', title='HRDP', tableset=tableset, columnset=columnset)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # print(":::::::::::::::", form.validate_on_submit())
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
        # after creating, user goes to login page (login_plain is func nane)
        return redirect(url_for('login_plain'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login/plain', methods=['GET', 'POST'])
def login_plain():
    # if logged in, go to
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# @app.route('/login/oauth')
# def index():
#     if oauth_google.is_logged_in():
#         user_info = oauth_google.get_user_info()
#         return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info,
#                                                                                                             indent=4) + "</pre>"
#
#     return 'You are not currently logged in.'


# logout & redirect to login plain
@app.route('/logout')
def logout():
    # session 날리기
    logout_user()
    return redirect(url_for('login_plain'))


# saving profile pic in server file system
def saving_pic(form_picture):
    # secret import for random pic file name
    random_hex = secrets.token_hex(8)
    # in order to get file extension, os import, and splitext func return two values
    _, file_ext = os.path.splitext(form_picture.filename)  # when using only on value, the other one should be _
    # making new file name
    new_picture_filename = random_hex + file_ext
    # making path to store new pic
    picture_path = os.path.join(app.root_path, 'static/profile_pics', new_picture_filename)
    print("::::::::::::::::::", picture_path)
    # before saving the pic, resizing using PIL import Image
    pixel_size = (122, 122)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(pixel_size)
    # saving new picture in the path
    resized_image.save(picture_path)

    return new_picture_filename


# get: visiting site, post: form submit
@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # User model : image_file column
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # pass the parameter into the template
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# page에 들어갔을때 GET, 입력할때는 POST
@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def creating_post():
    # form을 form wtf을 이용한 forms.py에서 가져와 쓴다. (form은 하나의 클래스에서 가져옴)
    form = PostForm()
    # wtf의 class기반의 form을 가져와서 submit한 녀석을 validation
    print("::::creating post:::", form.title.data)
    print("::::creating post:::", form.content.data)
    # print(":::::::", form.validate_on_submit())
    if form.validate_on_submit():
        # DB에 저장, Post from model
        print("============= inside===========")
        print(current_user)
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!!!', 'success')
        return redirect(url_for('home'))
    # rendering할때 form에다가 wtf에서 만들어낸 클래스를 기반으로 그녀석을 rendering한다.
    return render_template('post_template.html', title='New Post', form=form, legend="New Post")


# int: type (안써도 된다 - more specific하게 지정한것)
@app.route("/post/<int:post_id>")
# @app.route("/post/post_id")
def post(post_id):
    # get_or_404 is relative of get(), 404 is not found
    # post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def updating_post(post_id):
    post = Post.query.get_or_404(post_id)
    # after updating the post
    if post.author != current_user:
        abort(403)  # forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been update!', 'success')
        # redirect to detail page
        return redirect(url_for('post', post_id=post_id))
    # before updating the post
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post_template.html', title='Updating Post', form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=['POST'])  # POST only
@login_required
def deleting_post(post_id):
    post = Post.query.get_or_404(post_id)
    # after updating the post
    if post.author != current_user:
        abort(403)  # forbidden route
    # persistent work for deletion
    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/users/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query \
        .filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)



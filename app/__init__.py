# file name : __init__.py
# path : /hrdpflask/app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# import google.oauth2.credentials

# import oauth_google
# TODO: config files

app = Flask(__name__)
app.config['SECRET_KEY'] = '622eddbc87aa89d096fefb08c8460a65'
# /// relative path from current file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrdp.sdb'

# db instance
db = SQLAlchemy(app)
# hash
bcrypt = Bcrypt(app)
# session
login_manager = LoginManager(app)
# function name (config for login first required pages 'login_plain -> users.login_plain due to Blueprint)
login_manager.login_view = 'users.login_plain'
# flash message for bootstrap
login_manager.login_message_category= '_info_'
# after login, going to the page client visited

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# fetching EMAIL_USER, EMAIL_PASSWORD from env variable
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_USERNAME'] = 'attobes@gmail.com'
app.config['MAIL_PASSWORD'] = 'Panjung@@gl2'
mail = Mail(app)

from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main
from app.data.routes import data

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(data)

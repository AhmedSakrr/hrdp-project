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
# function name (config for login first required pages)
login_manager.login_view = 'login_plain'
# flash message for bootstrap
login_manager.login_message_category= '_info_'
# after login, going to the page client visited

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

from app import routes

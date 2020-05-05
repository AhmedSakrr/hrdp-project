# file name : __init__.py
# path : /hrdpflask/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_mysqldb import MySQL
from app.config import Config


# import google.oauth2.credentials

# import oauth_google
# TODO: config files

# these two lines move to create_app() inside
# app = Flask(__name__)
# app.config.from_object(Config)

mysql = MySQL()
# db instance
db = SQLAlchemy()
# hash
bcrypt = Bcrypt()
# session
login_manager = LoginManager()
# function name (config for login first required pages 'login_plain -> users.login_plain due to Blueprint)
login_manager.login_view = 'users.login_plain'
# flash message for bootstrap
login_manager.login_message_category= '_info_'
# after login, going to the page client visited
mail = Mail()

# these lines move to create_app() inside
# from app.users.routes import users
# from app.posts.routes import posts
# from app.main.routes import main
# from app.data.routes import data
#
# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)
# app.register_blueprint(data)

# app 대신에 이제 create_app() 사용
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # db instance
    db.init_app(app)
    # hash
    bcrypt.init_app(app)
    # session
    login_manager.init_app(app)
    mail.init_app(app)
    mysql.init_app(app)


    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from app.data.routes import data
    from app.errors.error_handlers import errors # instance of Blueprint in __init__.py
    from app.visuals.routes import visuals

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(data)
    app.register_blueprint(errors)
    app.register_blueprint(visuals)

    return app



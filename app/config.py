# class based config in a single object

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # app.config['SECRET_KEY'] = '622eddbc87aa89d096fefb08c8460a65'
    # # /// relative path from current file
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrdp.sdb'
    #
    # # app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    # # app.config['MAIL_PORT'] = 587
    # # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USE_SSL'] = True
    # # fetching EMAIL_USER, EMAIL_PASSWORD from env variable
    # # app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    # # app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
    # app.config['MAIL_USERNAME'] = '@gmail.com'
    # app.config['MAIL_PASSWORD'] = ''

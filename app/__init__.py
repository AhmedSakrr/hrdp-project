from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hrdp.sdb'

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # db instance
    db.init_app(app)

    from app.data.routes import data
    from app.errors.error_handlers import errors

    app.register_blueprint(data)
    app.register_blueprint(errors)

    return app



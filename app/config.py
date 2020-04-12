# class based config in a single object

import os


class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///hrdp.sdb'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

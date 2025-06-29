import os

class Config(object):

    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///test.db")
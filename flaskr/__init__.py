
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.globals import g
import tomllib

from .models import db,Posts
from . import views
from . import auth

def create_app():

    app = Flask(__name__,instance_relative_config=True)

    app.config.from_file('configs.toml',load=tomllib.load,text=False)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(views.bp)
    app.register_blueprint(auth.auth)

    auth.login_manager.init_app(app)

    return app

#O SSL_CONTEXT=ADHOC faz o servidor rodar em HTTPS
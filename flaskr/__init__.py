from flask import Flask
from dotenv import load_dotenv

from .models.models import db,ma
from .routes import views,auth,gposts

def create_app():
    load_dotenv()
    app = Flask(__name__)

    from .configs.base import Config
    app.config.from_object(Config)

    ma.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(views.bp)
    app.register_blueprint(auth.auth)
    app.register_blueprint(gposts.gp)

    auth.login_manager.init_app(app)

    return app


from flask import Flask, current_app, make_response, Response
from flask.globals import g
import tomllib

app = Flask(__name__,instance_relative_config=True)

app.config.from_file('configs.toml',load=tomllib.load,text=False)

from .db import db,Cadastrou
with app.app_context():
    db.init_app(app)
    db.create_all()

from . import views
app.register_blueprint(views.bp)

if __name__ == "__main__":
    app.run(debug=True)

#O SSL_CONTEXT=ADHOC faz o servidor rodar em HTTPS
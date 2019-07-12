from flask import Flask
from flask_migrate import Migrate

from api import bp


def create_app(config_file=None):
    app = Flask(__name__)
    if config_file is None:
        config_file = 'config.py'
    app.config.from_pyfile(config_file)

    from database import db
    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(bp, url_prefix='/api')

    return app

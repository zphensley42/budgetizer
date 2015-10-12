import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    # SQLAlchemy setup
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_MIGRATE_REPO'] = SQLALCHEMY_MIGRATE_REPO

    # Load default config and override config from an environment variable
    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
    ))
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    db.init_app(app)
    Bootstrap(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    # Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api_common as api_common_blueprint
    app.register_blueprint(api_common_blueprint, url_prefix='/api/')

    from .api.v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app

from automated_survey_flask.config import config_env_files
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
env = app.config.get("ENV", "production")


def prepare_app(environment=env, p_db=db):
    app.config.from_object(config_env_files[environment])
    p_db.init_app(app)
    # load views by importing them
    from . import views  # noqa F401

    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()


db.save = save_and_commit

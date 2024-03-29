import os

from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate
from flask_mail import Mail

from app.logger import log
from app.controllers import S3Bucket
from .database import db

# instantiate extensions
login_manager = LoginManager()
migration = Migrate()
mail = Mail()
s3bucket = S3Bucket()


def create_app(environment="development"):
    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
        user_blueprint,
        pest_blueprint,
        illness_blueprint,
        plant_family_blueprint,
        plant_varieties_blueprint,
        photos_blueprint,
        planting_program_blueprint,
        planting_step_type_blueprint,
        plant_category_blueprint,
        program_step_blueprint,
        category_blueprint,
        recipe_blueprint,
        recipe_step_blueprint,
    )
    from app import models as m

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("APP_ENV", environment)
    configuration = config(env)
    assert not configuration.IS_API
    app.config.from_object(configuration)
    configuration.configure(app)
    log(log.INFO, "Configuration: [%s]", configuration.ENV)

    # Set up extensions.
    db.init_app(app)
    migration.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    s3bucket.init_app(configuration)
    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(pest_blueprint)
    app.register_blueprint(illness_blueprint)
    app.register_blueprint(plant_family_blueprint)
    app.register_blueprint(plant_varieties_blueprint)
    app.register_blueprint(photos_blueprint)
    app.register_blueprint(planting_program_blueprint)
    app.register_blueprint(planting_step_type_blueprint)
    app.register_blueprint(plant_category_blueprint)
    app.register_blueprint(program_step_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(recipe_blueprint)
    app.register_blueprint(recipe_step_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id: int):
        query = m.User.select().where(m.User.id == int(id))
        return db.session.scalar(query)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = m.AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    return app

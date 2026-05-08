from flask import Flask
from db.models import db
import os


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    )


    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'exercises.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(db_path)}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "change-this-before-production"  # Replace with a secure key

    db.init_app(app)

    from agent_api.routes import register_blueprints

    register_blueprints(app)

    with app.app_context():
        db.create_all()
        from db.seed import seed
        seed()

    return app

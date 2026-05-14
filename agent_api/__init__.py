from flask import Flask
from db.models import db
import os


def create_app():
    # Get the project root directory (parent of agent_api)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static"),
    )

    # Ensure instance directory exists
    instance_dir = os.path.join(project_root, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    db_path = os.path.join(instance_dir, 'exercises.db')
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

from .auth_routes import auth_bp
from .workout_routes import workout_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(workout_bp)

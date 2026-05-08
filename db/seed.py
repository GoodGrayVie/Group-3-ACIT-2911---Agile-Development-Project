import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash

# --- PATH FIX ---
# This adds the main project folder to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we import models directly since we added the parent folder to the path
try:
    from db.models import db, MuscleGroup, Exercise, CardioExercise, User
except ModuleNotFoundError:
    from models import db, MuscleGroup, Exercise, CardioExercise, User

def seed():
    """
    Creates tables and populates the database with initial data.
    """
    db.create_all()
    print("Checked/Created all database tables.")

    # 1. Seed Muscle Groups
    muscle_groups = ["Chest", "Back", "Shoulders", "Biceps", "Triceps", "Legs", "Core", "Glutes"]
    for name in muscle_groups:
        if not MuscleGroup.query.filter_by(name=name).first():
            db.session.add(MuscleGroup(name=name))
    db.session.commit()

    # 2. Seed Exercises
    exercises = [
        ("Bench Press",            "Chest"),
        ("Incline Dumbbell Press", "Chest"),
        ("Cable Fly",              "Chest"),
        ("Pull Up",                "Back"),
        ("Bent Over Row",          "Back"),
        ("Lat Pulldown",           "Back"),
        ("Overhead Press",         "Shoulders"),
        ("Lateral Raise",          "Shoulders"),
        ("Face Pull",              "Shoulders"),
        ("Barbell Curl",           "Biceps"),
        ("Hammer Curl",            "Biceps"),
        ("Preacher Curl",          "Biceps"),
        ("Tricep Pushdown",        "Triceps"),
        ("Skull Crusher",          "Triceps"),
        ("Dip",                    "Triceps"),
        ("Squat",                  "Legs"),
        ("Romanian Deadlift",      "Legs"),
        ("Leg Press",              "Legs"),
        ("Plank",                  "Core"),
        ("Cable Crunch",           "Core"),
        ("Hip Thrust",             "Glutes"),
        ("Glute Kickback",         "Glutes"),
    ]
    for name, group_name in exercises:
        if not Exercise.query.filter_by(name=name).first():
            group = MuscleGroup.query.filter_by(name=group_name).first()
            if group:
                db.session.add(Exercise(name=name, muscle_group_id=group.id))
    db.session.commit()

    cardio_exercises = [
        "Running",
        "Cycling",
        "Rowing",
        "Swimming",
        "Jump Rope",
        "Elliptical",
        "Stair Climber",
        "Walking",
    ]

    for name in cardio_exercises:
        if not CardioExercise.query.filter_by(name=name).first():
            db.session.add(CardioExercise(name=name))
    db.session.commit()

    print("Seeded muscle groups, exercises, and cardio exercises.")
    # 3. Seed Test Users
    test_users = [
        {"name": "austin", "email": "austin@test.com", "hashed_password": generate_password_hash("password123")},
        {"name": "Ishaan", "email": "purewalishaan@gmail.com", "hashed_password": generate_password_hash("password123")}
    ]

    for u in test_users:
        if not User.query.filter_by(email=u["email"]).first():
            db.session.add(User(**u))
    
    db.session.commit()
    print("Successfully seeded database!")

if __name__ == "__main__":
    app = Flask(__name__)
    # Path to exercises.db
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../exercises.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        seed()
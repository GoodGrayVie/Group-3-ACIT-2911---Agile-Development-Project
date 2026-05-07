from werkzeug.security import generate_password_hash
from models import db, MuscleGroup, Exercise, CardioExercise, User


def seed():
    muscle_groups = [
        "Chest", "Back", "Shoulders", "Biceps",
        "Triceps", "Legs", "Core", "Glutes"
    ]

    for name in muscle_groups:
        if not MuscleGroup.query.filter_by(name=name).first():
            db.session.add(MuscleGroup(name=name))
    db.session.commit()

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

test_users = [
    {"name": "austin", "email": "austin@test.com", "hashed_password": generate_password_hash("password123")},
    {"name": "victor",   "email": "victor@test.com",   "hashed_password": generate_password_hash("password123")},
    {"name": "admin", "email": "admin@test.com", "hashed_password": generate_password_hash("admin123")},
]

for u in test_users:
    if not User.query.filter_by(name=u["name"]).first():
        db.session.add(User(**u))
db.session.commit()


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        seed()
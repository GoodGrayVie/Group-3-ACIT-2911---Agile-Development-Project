from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MuscleGroup(db.Model):
    __tablename__ = "muscle_groups"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    exercises = db.relationship("Exercise", backref="muscle_group", lazy=True)

class Exercise(db.Model):
    __tablename__ = "exercises"
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group_id  = db.Column(db.Integer, db.ForeignKey("muscle_groups.id"), nullable=False)
    description      = db.Column(db.Text, nullable=True)

class CardioExercise(db.Model):
    __tablename__ = "cardio_exercises"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Workout(db.Model):
    __tablename__ = "workouts"
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    date  = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    sets   = db.relationship("WorkoutSet", backref="workout", lazy=True)
    cardio = db.relationship("WorkoutCardio", backref="workout", lazy=True)

class WorkoutSet(db.Model):
    __tablename__ = "workout_sets"
    id          = db.Column(db.Integer, primary_key=True)
    workout_id  = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    set_number  = db.Column(db.Integer, nullable=False)
    reps        = db.Column(db.Integer, nullable=False)
    weight      = db.Column(db.Float, nullable=False)
    weight_unit = db.Column(db.String(2), nullable=False, default="kg")
    exercise    = db.relationship("Exercise", backref="workout_sets")

class WorkoutCardio(db.Model):
    __tablename__ = "workout_cardio"
    id          = db.Column(db.Integer, primary_key=True)
    workout_id  = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("cardio_exercises.id"), nullable=False)
    duration    = db.Column(db.Integer, nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    hashed_password = db.Column(db.String(200), nullable=False)
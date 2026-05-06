from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
from db.models import (
    db,
    Workout,
    MuscleGroup,
    Exercise,
    CardioExercise,
    WorkoutCardio,
    WorkoutSet,
)
import json


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exercises.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "change-this-before-production"  # Replace with a secure key
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

# --------------------------------------------------------------------------

# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def home():
    """
    Home page — always goes straight to the dashboard.
    Login is optional via the header button.
    """
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page — updated to capture username and password.
    Redirects to dashboard once submitted.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username and password:
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Please enter both a username and password.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """
    Main dashboard — always renders for any visitor.
    Passes username and workouts if logged in, None/[] if not.

    Template receives:
        username (str | None)    – logged-in user's name, or None
        workouts (list[dict])    – workout history, or empty list
    """
    username = session.get("username")

    workouts = Workout.query.order_by(Workout.date.desc()).limit(20).all()
    return render_template("dashboard.html", username=username, workouts=workouts)


@app.route("/workouts/add", methods=["GET", "POST"], endpoint="log_workout")
def log_workout():
    if request.method == "GET":
        exercises = Exercise.query.order_by(Exercise.name).all()
        cardio_exercises = CardioExercise.query.order_by(CardioExercise.name).all()

        exercises_json = json.dumps(
            [{"id": ex.id, "name": ex.name} for ex in exercises]
        )

        return render_template(
            "log_workout.html",
            exercises=exercises,
            cardio_exercises=cardio_exercises,
            exercises_json=exercises_json,
        )

    # -----------------------------
    #  Save workout
    # -----------------------------
    name = request.form.get("name")
    date_str = request.form.get("date")
    notes = request.form.get("notes")

    # Convert date
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Create workout
    workout = Workout(name=name, date=date, notes=notes)
    db.session.add(workout)
    db.session.flush()

    # -----------------------------
    # Weight training Sets
    # -----------------------------
    exercise_ids = request.form.getlist("exercise_id[]")
    set_numbers = request.form.getlist("set_number[]")
    reps_list = request.form.getlist("reps[]")
    weights = request.form.getlist("weight[]")
    weight_units = request.form.getlist("weight_unit[]")
    heart_rates = request.form.getlist("set_heart_rate[]")

    for i in range(len(exercise_ids)):
        if not exercise_ids[i]:
            continue

        set_entry = WorkoutSet(
            workout_id=workout.id,
            exercise_id=int(exercise_ids[i]),
            set_number=int(set_numbers[i]),
            reps=int(reps_list[i]),
            weight=float(weights[i]),
            weight_unit=weight_units[i],
            heart_rate=int(heart_rates[i]) if heart_rates[i] else None,
        )
        db.session.add(set_entry)

    # -----------------------------
    # Cardio Entries
    # -----------------------------
    cardio_ids = request.form.getlist("cardio_exercise_id[]")
    durations = request.form.getlist("duration[]")
    distances = request.form.getlist("distance[]")
    cardio_hr = request.form.getlist("cardio_heart_rate[]")

    for i in range(len(cardio_ids)):
        if not cardio_ids[i]:
            continue

        cardio_entry = WorkoutCardio(
            workout_id=workout.id,
            exercise_id=int(cardio_ids[i]),
            duration=int(durations[i]),
            distance=float(distances[i]) if distances[i] else None,
            heart_rate=int(cardio_hr[i]) if cardio_hr[i] else None,
        )
        db.session.add(cardio_entry)

    # Commit everything
    db.session.commit()

    return redirect(url_for("dashboard"))


@app.route("/workouts/<int:workout_id>")
def view_workout(workout_id):
    """Show all detail for a single workout."""
    workout = Workout.query.get_or_404(workout_id)
    return render_template("workout_detail.html", workout=workout)


# @app.route("/log-workout", methods=["GET", "POST"])
# def log_workout():
#     """
#     Log a new workout.
#     GET  – renders the log-workout form (teammate's template).
#     POST – validates and saves the workout, then redirects to dashboard.

#     Expected form fields:
#         date     (str)  e.g. "2026-04-29"
#         type     (str)  e.g. "Running"
#         length   (str)  e.g. "45"  (minutes)
#         calories (str)  e.g. "320"
#     """
#     if "username" not in session:
#         return redirect(url_for("login"))

#     if request.method == "POST":
#         errors = []

#         date_str = request.form.get("date", "").strip()
#         wtype = request.form.get("type", "").strip()
#         length = request.form.get("length", "").strip()
#         calories = request.form.get("calories", "").strip()

#         # --- Basic validation ---
#         if not date_str:
#             errors.append("Date is required.")
#         else:
#             try:
#                 datetime.strptime(date_str, "%Y-%m-%d")
#             except ValueError:
#                 errors.append("Date must be in YYYY-MM-DD format.")

#         if not wtype:
#             errors.append("Workout type is required.")

#         if not length:
#             errors.append("Length is required.")
#         else:
#             try:
#                 length = int(length)
#                 if length <= 0:
#                     raise ValueError
#             except ValueError:
#                 errors.append("Length must be a positive whole number (minutes).")

#         if not calories:
#             errors.append("Calories burnt is required.")
#         else:
#             try:
#                 calories = int(calories)
#                 if calories < 0:
#                     raise ValueError
#             except ValueError:
#                 errors.append("Calories must be a non-negative whole number.")

#         if errors:
#             for error in errors:
#                 flash(error)
#             return render_template("log_workout.html")

#         workout = {
#             "date": date_str,
#             "type": wtype,
#             "length": length,
#             "calories": calories,
#         }
#         add_workout(session["username"], workout)
#         flash("Workout logged successfully!")
#         return redirect(url_for("dashboard"))

#     return render_template("log_workout.html")


@app.route("/logout")
def logout():
    """Clear the session and return to the dashboard."""
    session.clear()
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------------------
# Dev entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

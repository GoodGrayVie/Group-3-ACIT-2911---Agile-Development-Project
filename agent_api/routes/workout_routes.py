from flask import render_template, redirect, url_for, request, Blueprint, jsonify, session
from datetime import datetime
from db.models import (
    db,
    Workout,
    Exercise,
    CardioExercise,
    WorkoutCardio,
    WorkoutSet,
    User
)
import json

workout_bp = Blueprint("workout", __name__)


@workout_bp.route("/workouts/add", methods=["GET", "POST"], endpoint="log_workout")
def log_workout():
    if not session.get("username"):
        return redirect(url_for("auth.login"))
    if request.method == "GET":
        weight_exercises = Exercise.query.order_by(Exercise.name).all()
        cardio_exercises = CardioExercise.query.order_by(CardioExercise.name).all()

        exercises_json = json.dumps({
    "weights": [
        {
            "id": ex.id,
            "name": ex.name,
            "muscle_group": ex.muscle_group.name
        } for ex in weight_exercises
    ],
    "cardio": [
        {"id": ex.id, "name": ex.name} for ex in cardio_exercises
    ]
})

        return render_template("log_workout.html", exercises_json=exercises_json, username=session.get("username"))
       

    # -----------------------------
    #  Save workout
    # -----------------------------
    name = request.form.get("name")
    date_str = request.form.get("date")
    notes = request.form.get("notes")

    # Convert date
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Create workout
    user = User.query.filter_by(name=session.get("username")).first()
    workout = Workout(name=name, date=date, notes=notes, user_id=user.id)
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
    # Cardio
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
    print("FORM DATA:", request.form)
    print("WORKOUT SETS:", workout.sets)
    print("WORKOUT CARDIO:", workout.cardio)

    return redirect(url_for("auth.dashboard"))


@workout_bp.route("/workouts/<int:workout_id>")
def view_workout(workout_id):
    """Show all detail for a single workout.
    Workouts are only visible to the User who created that workout
    """
    if not session.get("username"):
        return redirect(url_for("auth.login"))
    workout = Workout.query.get_or_404(workout_id)
    return render_template("workout_detail.html", workout=workout, username=session.get("username"))

@workout_bp.route("/workouts/<int:workout_id>/delete", methods=["POST"])
def delete_workout(workout_id):
    if not session.get("username"):
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(name=session.get("username")).first()
    workout = Workout.query.filter_by(id=workout_id, user_id=user.id).first_or_404()

    db.session.delete(workout)
    db.session.commit()

    return redirect(url_for("auth.dashboard"))


@workout_bp.route("/view-progress")
def view_progress():
    return render_template("view_workout.html")


@workout_bp.route("/view-progress/exercises")
def get_exercises():
    strength = Exercise.query.order_by(Exercise.name).all()
    cardio = CardioExercise.query.order_by(CardioExercise.name).all()

    return jsonify(
        {
            "strength": [{"id": ex.id, "name": ex.name} for ex in strength],
            "cardio": [{"id": ex.id, "name": ex.name} for ex in cardio],
        }
    )


@workout_bp.route("/view-progress/data")
def progress_data():
    exercise_id = request.args.get("exercise_id", type=int)
    exercise_type = request.args.get("type")  # "strength" or "cardio"
    stat = request.args.get("stat")
    year = request.args.get("year", type=int)

    if exercise_type == "strength":
        query = (
            db.session.query(WorkoutSet, Workout.date)
            .join(Workout, WorkoutSet.workout_id == Workout.id)
            .filter(WorkoutSet.exercise_id == exercise_id)
        )
    else:
        query = (
            db.session.query(WorkoutCardio, Workout.date)
            .join(Workout, WorkoutCardio.workout_id == Workout.id)
            .filter(WorkoutCardio.exercise_id == exercise_id)
        )

    if year:
        query = query.filter(db.extract("year", Workout.date) == year)

    query = query.order_by(Workout.date).all()

    labels = [row[1].strftime("%Y-%m-%d") for row in query]

    values = [getattr(row[0], stat) for row in query]

    return jsonify({"labels": labels, "values": values})

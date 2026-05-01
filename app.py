from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-before-production"  # Replace with a secure key

# ---------------------------------------------------------------------------
# Temporary in-memory store — swap for a real DB (SQLite, Postgres, etc.)
# ---------------------------------------------------------------------------
workout_store: dict[str, list[dict]] = {}


def get_user_workouts(username: str) -> list[dict]:
    """Return the workout history for a given user."""
    return workout_store.get(username, [])


def add_workout(username: str, workout: dict) -> None:
    """Append a new workout entry for a given user."""
    workout_store.setdefault(username, []).append(workout)


# ---------------------------------------------------------------------------
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
    workouts = get_user_workouts(username) if username else []

    return render_template("dashboard.html", username=username, workouts=workouts)


@app.route("/log-workout", methods=["GET", "POST"])
def log_workout():
    """
    Log a new workout.
    GET  – renders the log-workout form (teammate's template).
    POST – validates and saves the workout, then redirects to dashboard.

    Expected form fields:
        date     (str)  e.g. "2026-04-29"
        type     (str)  e.g. "Running"
        length   (str)  e.g. "45"  (minutes)
        calories (str)  e.g. "320"
    """
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        errors = []

        date_str  = request.form.get("date", "").strip()
        wtype     = request.form.get("type", "").strip()
        length    = request.form.get("length", "").strip()
        calories  = request.form.get("calories", "").strip()

        # --- Basic validation ---
        if not date_str:
            errors.append("Date is required.")
        else:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                errors.append("Date must be in YYYY-MM-DD format.")

        if not wtype:
            errors.append("Workout type is required.")

        if not length:
            errors.append("Length is required.")
        else:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                errors.append("Length must be a positive whole number (minutes).")

        if not calories:
            errors.append("Calories burnt is required.")
        else:
            try:
                calories = int(calories)
                if calories < 0:
                    raise ValueError
            except ValueError:
                errors.append("Calories must be a non-negative whole number.")

        if errors:
            for error in errors:
                flash(error)
            return render_template("log_workout.html")

        workout = {
            "date":     date_str,
            "type":     wtype,
            "length":   length,
            "calories": calories,
        }
        add_workout(session["username"], workout)
        flash("Workout logged successfully!")
        return redirect(url_for("dashboard"))

    return render_template("log_workout.html")


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
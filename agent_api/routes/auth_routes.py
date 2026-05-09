from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from db.models import Workout, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    """
    Home page — always goes straight to the dashboard.
    Login is optional via the header button.
    """
    return redirect(url_for("auth.dashboard"))


@auth_bp.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("auth.dashboard"))

        flash("Please enter both a username and password.")

    return render_template("login.html")


@auth_bp.route("/dashboard")
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


@auth_bp.route("/logout")
def logout():
    """Clear the session and return to the dashboard."""
    session.clear()
    return redirect(url_for("auth.dashboard"))

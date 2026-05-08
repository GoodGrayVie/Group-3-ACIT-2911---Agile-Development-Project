from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from db.models import Workout, User
from werkzeug.security import check_password_hash

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
    if request.method == "POST":
        # Match 'name="username"' from your login.html
        u_input = request.form.get("username", "").strip()
        p_input = request.form.get("password", "").strip()
        
        # Check database for user
        user = User.query.filter((User.name == u_input) | (User.email == u_input)).first()
        
        if user and check_password_hash(user.hashed_password, p_input):
            session["username"] = user.name
            flash(f"Logged in as {user.name}")
            return redirect(url_for("auth.dashboard"))

        flash("Invalid Credentials")
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

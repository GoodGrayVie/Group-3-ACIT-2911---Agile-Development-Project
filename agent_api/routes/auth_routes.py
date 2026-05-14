from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from db.models import Workout, User, db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return redirect(url_for("auth.dashboard"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u_input = request.form.get("username", "").strip()
        p_input = request.form.get("password", "").strip()

        user = User.query.filter(
            (User.name == u_input) | (User.email == u_input)
        ).first()

        if user and check_password_hash(user.hashed_password, p_input):
            session["username"] = user.name
            flash(f"Logged in as {user.name}")
            return redirect(url_for("auth.dashboard"))

        flash("Invalid Credentials")
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("All fields are required")
            return render_template("register.html")

        existing_user = User.query.filter(
            (User.name == name) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session["username"] = name
        flash(f"Registered and logged in as {name}")
        return redirect(url_for("auth.dashboard"))

    return render_template("register.html")


@auth_bp.route("/dashboard")
def dashboard():
    username = session.get("username")
    workouts = []
    if username:
        user = User.query.filter_by(name=username).first()
        if user:
            workouts = Workout.query.filter_by(user_id=user.id).order_by(Workout.date.desc()).limit(20).all()
    return render_template("dashboard.html", username=username, workouts=workouts)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.dashboard"))

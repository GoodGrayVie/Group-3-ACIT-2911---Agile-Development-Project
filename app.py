from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash
from db.models import db, User
import os

app = Flask(__name__)
app.secret_key = "ishaan-project-secret"

# Database path setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'exercises.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# In-memory history (Linked to usernames)
workout_store = {}

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("dashboard"))
        
        flash("Invalid Credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    
    user = session["username"]
    # LINKED HISTORY: Only get workouts for this specific user
    user_workouts = workout_store.get(user, [])
    return render_template("dashboard.html", username=user, workouts=user_workouts)

@app.route("/log-workout", methods=["GET", "POST"])
def log_workout():
    if "username" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        user = session["username"]
        new_workout = {
            "type": request.form.get("type"),
            "date": request.form.get("date"),
            "length": request.form.get("length")
        }
        # Add to this user's specific history
        if user not in workout_store:
            workout_store[user] = []
        workout_store[user].append(new_workout)
        
        flash("Workout logged!")
        return redirect(url_for("dashboard"))
    return render_template("log_workout.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

Hello hello! Welcome to our group repository. Let's have all memebers write their name in this file, followed by their student number.

Group Members:
Grayson Plug | A01459356
Victor Sebellin | A01488229
Austin Schmidt | A01488228
Phoenix Matticks | A01424183
Ishaandeep Purewal | A01487674

## Project Structure
```
Fitness app/
├── app.py                          # run app here
├── pyproject.toml
├── .gitignore
│
├── db/
│   ├── models.py                   # SQLAlchemy models
│   └── seed.py                     # initial data
│
├── agent_api/
|   ├── routes/
|   |   ├── __init__.py        # blueprint - auth_bp & workout_bp
|   |   ├── auth_routes.py     # login and dashboard routing
|   |   └── workout_routes.py  # log workouts routing
│   └── __init__.py            # create app Flask Blueprint
│
├── auth/
│   ├── __init__.py
│   └── auth.py                    /login, /logout, /register authentication checker
│
├── templates/
│   ├── base.html                   # shared layout
│   ├── dashboard.html
│   ├── login.html
│   └── log_workout.html
│
├── static/
│   ├── styles/
│   │   └── styles.css
│   └── js/
│       └── log_workout.js
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    ├── test_workouts.py
    └── test_exercises.py
```
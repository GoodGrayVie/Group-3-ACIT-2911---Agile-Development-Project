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
├── app.py                          # app factory, registers blueprints
├── pyproject.toml
├── .gitignore
│
├── db/
│   ├── models.py                   # SQLAlchemy models
│   └── seed.py                     # initial data
│
├── workouts/
│   ├── __init__.py
│   └── routes.py                   # blueprint: /log-workout
│
├── auth/
│   ├── __init__.py
│   └── auth.py                     # blueprint: /login, /logout, /register
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

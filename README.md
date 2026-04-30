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
├── app.py                          #flask routes (this should be changed to multiple probably)
├── pyproject.toml
├── database.py                     #SQLite connection
├──exercises.db #database
├── templates/                      #html pages
│   ├── home.html
│   ├── login.html
│   ├── workout_history.html
│   ├── add_workout.html
├── auth/
│   ├── auth.py
│   ├──
│   └──
├── styles
│   ├──styles.css
│
└── tests/
    ├── __init__.py
    ├── conftest.py            # Shared test fixtures (fake psutil data)
    ├── test_auth.py
    ├── test_workouts.py        # Tests for the Monitor class
    └── test_exercises.py      # Tests for the API endpoints
```

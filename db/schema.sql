-- Muscle Groups
CREATE TABLE IF NOT EXISTS muscle_groups (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE
);

-- Exercises
CREATE TABLE IF NOT EXISTS exercises (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT NOT NULL UNIQUE,
    muscle_group_id  INTEGER NOT NULL,
    description      TEXT,
    FOREIGN KEY (muscle_group_id) REFERENCES muscle_groups(id)
);
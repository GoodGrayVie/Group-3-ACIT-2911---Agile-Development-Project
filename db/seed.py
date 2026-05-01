from models import db, MuscleGroup, Exercise


def seed():
    db.connect(reuse_if_open=True)
    db.create_tables([MuscleGroup, Exercise])

    muscle_groups = [
        "Chest", "Back", "Shoulders", "Biceps",
        "Triceps", "Legs", "Core", "Glutes"
    ]

    for name in muscle_groups:
        MuscleGroup.get_or_create(name=name)

    exercises = [
        ("Bench Press",             "Chest",     "Barbell press lying flat on a bench"),
        ("Incline Dumbbell Press",  "Chest",     "Dumbbell press on an inclined bench"),
        ("Cable Fly",               "Chest",     "Chest fly using cable machine"),
        ("Pull Up",                 "Back",      "Bodyweight pull up on a bar"),
        ("Bent Over Row",           "Back",      "Barbell row hinged at the hips"),
        ("Lat Pulldown",            "Back",      "Cable pulldown targeting the lats"),
        ("Overhead Press",          "Shoulders", "Barbell press overhead from the shoulders"),
        ("Lateral Raise",           "Shoulders", "Dumbbell raise to the sides"),
        ("Face Pull",               "Shoulders", "Cable pull toward the face for rear delts"),
        ("Barbell Curl",            "Biceps",    "Standing curl with a barbell"),
        ("Hammer Curl",             "Biceps",    "Neutral grip dumbbell curl"),
        ("Preacher Curl",           "Biceps",    "Curl performed on a preacher bench"),
        ("Tricep Pushdown",         "Triceps",   "Cable pushdown targeting the triceps"),
        ("Skull Crusher",           "Triceps",   "Barbell extension lying on a bench"),
        ("Dip",                     "Triceps",   "Bodyweight dip on parallel bars"),
        ("Squat",                   "Legs",      "Barbell back squat"),
        ("Romanian Deadlift",       "Legs",      "Hip hinge deadlift with slight knee bend"),
        ("Leg Press",               "Legs",      "Machine press with legs"),
        ("Plank",                   "Core",      "Isometric core hold"),
        ("Cable Crunch",            "Core",      "Weighted crunch using cable machine"),
        ("Hip Thrust",              "Glutes",    "Barbell thrust driving through the glutes"),
        ("Glute Kickback",          "Glutes",    "Cable or bodyweight kickback for glutes"),
    ]

    for name, group_name, description in exercises:
        group = MuscleGroup.get(MuscleGroup.name == group_name)
        Exercise.get_or_create(name=name, defaults={
            "muscle_group": group,
            "description": description
        })

    print("Seeded muscle groups and exercises.")


if __name__ == "__main__":
    seed()
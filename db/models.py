# db/models.py
from peewee import *

db = SqliteDatabase("exercises.db")

class BaseModel(Model):
    class Meta:
        database = db

class MuscleGroup(BaseModel):
    name = CharField(unique=True)

class Exercise(BaseModel):
    name = CharField(unique=True)
    muscle_group = ForeignKeyField(MuscleGroup, backref="exercises")
    description = TextField(null=True)
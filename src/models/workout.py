from datetime import datetime, timedelta

from pydantic import BaseModel

from src.models.exercise import Exercise
from src.models.user import User


class Workout(BaseModel):
    id: int
    name: str
    description: str
    user: User
    workout_exercises: list["WorkoutExercise"]
    created_at: datetime
    updated_at: datetime


class WorkoutExercise(BaseModel):
    id: int
    workout: Workout
    exercise: Exercise
    break_time: timedelta
    created_at: datetime

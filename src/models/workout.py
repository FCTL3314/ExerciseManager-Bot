from datetime import datetime, timedelta

from pydantic import BaseModel

from src.models.exercise import NestedExercise
from src.models.user import User


class Workout(BaseModel):
    id: int
    name: str
    description: str
    user: User
    workout_exercises: list["NestedWorkoutExercise"]
    created_at: datetime
    updated_at: datetime


class WorkoutExercise(BaseModel):
    id: int
    workout: Workout
    exercise: NestedExercise
    break_time: timedelta
    created_at: datetime


class NestedWorkoutExercise(BaseModel):
    id: int
    exercise: NestedExercise
    break_time: timedelta
    created_at: datetime

from datetime import datetime, timedelta

from pydantic import BaseModel

from src.models import PaginatedResponse
from src.models.exercise import ExerciseRead
from src.models.user import User


class Workout(BaseModel):
    id: int
    name: str
    description: str
    user: User
    workout_exercises: list["WorkoutExerciseRead"]
    created_at: datetime
    updated_at: datetime


class WorkoutExercise(BaseModel):
    id: int
    workout: Workout
    exercise: ExerciseRead
    break_time: timedelta
    created_at: datetime


class WorkoutExerciseRead(BaseModel):
    id: int
    exercise: ExerciseRead
    break_time: timedelta
    created_at: datetime


class WorkoutPaginatedResponse(PaginatedResponse[Workout]): ...

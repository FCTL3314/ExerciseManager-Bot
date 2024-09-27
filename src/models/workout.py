from datetime import datetime, timedelta

from pydantic import BaseModel

from src.models import PaginatedResponse, create_timedelta_from_nanoseconds_validator
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

    @property
    def exercises_duration(self) -> timedelta:
        return sum(
            (
                workout_exercise.exercise.duration
                for workout_exercise in self.workout_exercises
            ),
            timedelta(),
        )

    @property
    def workout_duration(self) -> timedelta:
        return (
            sum(
                (exercise.break_time for exercise in self.workout_exercises),
                timedelta(),
            )
            + self.exercises_duration
        )

    @property
    def exercises_count(self) -> int:
        return len(self.workout_exercises)


class WorkoutExercise(BaseModel):
    id: int
    workout: Workout
    exercise: ExerciseRead
    break_time: timedelta
    created_at: datetime

    _break_time_from_nanoseconds = create_timedelta_from_nanoseconds_validator(
        "break_time"
    )


class WorkoutExerciseRead(BaseModel):
    id: int
    exercise: ExerciseRead
    break_time: timedelta
    created_at: datetime

    _break_time_from_nanoseconds = create_timedelta_from_nanoseconds_validator(
        "break_time"
    )


class WorkoutPaginatedResponse(PaginatedResponse[Workout]): ...

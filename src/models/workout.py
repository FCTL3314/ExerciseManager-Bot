from datetime import datetime, timedelta

from babel.dates import format_timedelta
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

    def get_humanized_exercises_duration(self, locale: str) -> str:
        return format_timedelta(self.exercises_duration, locale=locale)

    @property
    def workout_duration(self) -> timedelta:
        return (
            sum(
                (exercise.break_time for exercise in self.workout_exercises),
                timedelta(),
            )
            + self.exercises_duration
        )

    def get_humanized_workout_duration(self, locale: str) -> str:
        return format_timedelta(self.workout_duration, locale=locale)

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


class WorkoutSettings(BaseModel):
    pre_start_timer_seconds: int
    manual_mode_enabled: bool


class WorkoutState(BaseModel):
    workout_exercises: list[WorkoutExerciseRead]
    current_workout_exercise: WorkoutExerciseRead

    @property
    def is_first_exercise(self) -> bool:
        return self.current_exercise_index == 0

    @property
    def next_exercise_index(self) -> int:
        return self.current_exercise_index + 1

    @property
    def no_more_exercises(self) -> bool:
        return self.next_exercise_index >= len(self.workout_exercises)

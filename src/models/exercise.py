from datetime import timedelta

from babel.dates import format_timedelta
from pydantic import BaseModel

from src.models import (
    create_timedelta_from_nanoseconds_validator,
)
from src.models.user import User


class Exercise(BaseModel):
    id: int
    name: str
    description: str
    duration: timedelta
    image: str | None
    user: User

    _duration_from_nanoseconds = create_timedelta_from_nanoseconds_validator("duration")


class ExerciseRead(BaseModel):
    id: int
    name: str
    description: str
    duration: timedelta
    image: str | None

    _duration_from_nanoseconds = create_timedelta_from_nanoseconds_validator("duration")

    def get_humanized_duration(self, locale: str) -> str:
        return format_timedelta(self.duration, locale=locale)

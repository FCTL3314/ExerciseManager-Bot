from datetime import timedelta

from pydantic import BaseModel

from src.models.user import User


class Exercise(BaseModel):
    id: int
    name: str
    description: str
    duration: timedelta
    image: str | None
    user: User


class ExerciseRead(BaseModel):
    id: int
    name: str
    description: str
    duration: timedelta
    image: str | None

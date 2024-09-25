from abc import ABC, abstractmethod
from datetime import timedelta

from src.models.exercise import Exercise
from src.services.api import BaseAPIClient
from src.services.duration import to_nanoseconds


class IExerciseAPIClient(BaseAPIClient, ABC):
    @abstractmethod
    async def create(
        self, access_token: str, name: str, description: str, duration: timedelta
    ) -> Exercise: ...


class WorkoutAPIClient(IExerciseAPIClient):

    async def create(
        self, access_token: str, name: str, description: str, duration: timedelta
    ) -> Exercise:
        data = await self.request(
            "POST",
            "exercises/",
            data={
                "name": name,
                "description": description,
                "duration": to_nanoseconds(duration),
            },
            headers=await self.get_auth_header(access_token),
        )
        return Exercise(**data)

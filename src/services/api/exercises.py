from abc import ABC, abstractmethod

from src.models.exercise import Exercise
from src.services.api import BaseAPIClient


class IExerciseAPIClient(BaseAPIClient, ABC):
    @abstractmethod
    async def create(
        self, access_token: str, name: str, description: str, duration: int
    ) -> Exercise: ...


class DefaultExerciseAPIClient(IExerciseAPIClient):

    async def create(
        self, access_token: str, name: str, description: str, duration: int
    ) -> Exercise:
        data = await self.request(
            "POST",
            "exercises/",
            data={
                "name": name,
                "description": description,
                "duration": duration,
            },
            headers=await self.get_auth_header(access_token),
        )
        return Exercise(**data)

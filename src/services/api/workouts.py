from abc import ABC, abstractmethod

from src.models.workout import Workout
from src.services.api import BaseAPIClient


class IWorkoutAPIClient(BaseAPIClient, ABC):
    @abstractmethod
    async def create(
        self, access_token: str, name: str, description: str
    ) -> Workout: ...


class WorkoutAPIClient(IWorkoutAPIClient):

    async def create(self, access_token: str, name: str, description: str) -> Workout:
        data = await self.request(
            "POST",
            "workouts/",
            data={"name": name, "description": description},
            headers=await self.get_auth_header(access_token),
        )
        return Workout(**data)

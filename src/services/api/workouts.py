from abc import ABC, abstractmethod

from src.models.workout import Workout
from src.services.api import BaseAPIClient


class IWorkoutAPIClient(BaseAPIClient, ABC):
    @abstractmethod
    async def list(self, user_id: int | str | None) -> list[Workout]: ...

    @abstractmethod
    async def create(
        self, access_token: str, name: str, description: str
    ) -> Workout: ...

    @abstractmethod
    async def add_exercise(
        self,
        access_token: str,
        workout_id: int | str,
        exercise_id: int | str,
        break_time: int,
    ) -> Workout: ...


class DefaultWorkoutAPIClient(IWorkoutAPIClient):

    async def list(self, user_id: int | str | None) -> list[Workout]:
        params = {}
        if user_id is not None:
            params["user_id"] = user_id

        data = await self.request(
            "GET",
            "workouts/",
            params=params,
        )
        return [Workout(**workout) for workout in data["results"]]

    async def create(self, access_token: str, name: str, description: str) -> Workout:
        workout = await self.request(
            "POST",
            "workouts/",
            data={"name": name, "description": description},
            headers=await self.get_auth_header(access_token),
        )
        return Workout(**workout)

    async def add_exercise(
        self,
        access_token: str,
        workout_id: int | str,
        exercise_id: int | str,
        break_time: int,
    ) -> Workout:
        workout = await self.request(
            "POST",
            f"workouts/{workout_id}/exercises/add",
            data={"exercise_id": exercise_id, "break_time": break_time},
            headers=await self.get_auth_header(access_token),
        )
        return Workout(**workout)

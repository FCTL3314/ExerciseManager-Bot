from typing import Protocol, runtime_checkable

from src.models.workout import Workout, WorkoutPaginatedResponse
from src.services.api import BaseAPIClientProto, BaseAPIClient


@runtime_checkable
class WorkoutAPIClientProto(BaseAPIClientProto, Protocol):
    async def retrieve(self, workout_id: int | str) -> Workout: ...

    async def list(
        self,
        user_id: int | str | None,
        limit: int,
        offset: int,
    ) -> WorkoutPaginatedResponse: ...

    async def create(
        self, access_token: str, name: str, description: str
    ) -> Workout: ...

    async def add_exercise(
        self,
        access_token: str,
        workout_id: int | str,
        exercise_id: int | str,
        break_time: int,
    ) -> Workout: ...


class DefaultWorkoutAPIClient(BaseAPIClient):

    async def retrieve(self, workout_id: int | str) -> Workout:
        workout = await self.request("GET", f"workouts/{workout_id}/")
        return Workout(**workout)

    async def list(
        self,
        user_id: int | str | None,
        limit: int = 64,
        offset: int = 0,
    ) -> WorkoutPaginatedResponse:
        params = {"limit": limit, "offset": offset}
        if user_id is not None:
            params["user_id"] = user_id

        data = await self.request(
            "GET",
            "workouts/",
            params=params,
        )
        return WorkoutPaginatedResponse(
            count=data["count"],
            limit=data["limit"],
            offset=data["offset"],
            results=[Workout(**workout) for workout in data["results"]],
        )

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

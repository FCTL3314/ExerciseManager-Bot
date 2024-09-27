from mypy.semanal_shared import Protocol
from typing import runtime_checkable

from src.models.exercise import Exercise
from src.services.api import BaseAPIClientProto, BaseAPIClient


@runtime_checkable
class ExerciseAPIClientProto(BaseAPIClientProto, Protocol):
    async def create(
        self, access_token: str, name: str, description: str, duration: int
    ) -> Exercise: ...


class DefaultExerciseAPIClient(BaseAPIClient):

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

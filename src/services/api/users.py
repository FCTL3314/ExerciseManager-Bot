from typing import runtime_checkable

from mypy.semanal_shared import Protocol

from src.models.user import User
from src.services.api import BaseAPIClient, BaseAPIClientProto


@runtime_checkable
class UserAPIClientProto(BaseAPIClientProto, Protocol):
    async def me(self, access_token: str) -> User: ...


class DefaultUserAPIClient(BaseAPIClient):

    async def me(self, access_token: str) -> User:
        data = await self.request(
            "GET",
            "users/me/",
            headers=await self.get_auth_header(access_token),
        )
        return User(**data)

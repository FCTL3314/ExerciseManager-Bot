from abc import ABC, abstractmethod

from src.models.user import User
from src.services.api.client import APIClient


class IUserAPIClient(APIClient, ABC):
    @abstractmethod
    async def me(self, access_token: str) -> User: ...


class UserAPIClient(IUserAPIClient):

    async def me(self, access_token: str) -> User:
        data = await self.request(
            "GET",
            "users/me/",
            headers=await self.get_auth_header(access_token),
        )
        return User(**data)

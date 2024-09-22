from abc import ABC, abstractmethod

from src.models.auth import TokensResponse
from src.models.user import User
from src.services.api.client import APIClient


class IAuthAPIClient(APIClient, ABC):
    @abstractmethod
    async def register(self, username: str, password: str) -> User: ...

    @abstractmethod
    async def login(self, username: str, password: str) -> TokensResponse: ...

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> TokensResponse: ...


class AuthAPIClient(IAuthAPIClient):

    async def register(self, username: str, password: str) -> User:
        response = await self.request(
            "POST", "users/create/", data={"username": username, "password": password}
        )
        data = await response.json()
        return User(**data)

    async def login(self, username: str, password: str) -> TokensResponse:
        response = await self.request(
            "POST", "users/login/", data={"username": username, "password": password}
        )
        data = await response.json()
        return TokensResponse(**data)

    async def refresh_tokens(self, refresh_token: str) -> TokensResponse:
        response = await self.request(
            "POST", "users/refresh/", data={"refresh_token": refresh_token}
        )
        data = await response.json()
        return TokensResponse(**data)

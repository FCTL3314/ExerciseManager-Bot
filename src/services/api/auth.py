from abc import ABC, abstractmethod
from typing import Any

from src.models.auth import TokenRefreshResponse
from src.services.api.client import APIClient


class IAuthAPIClient(APIClient, ABC):
    @abstractmethod
    async def register(self, username: str, password: str) -> dict[str, Any]: ...

    @abstractmethod
    async def login(self, username: str, password: str) -> dict[str, Any]: ...

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> TokenRefreshResponse: ...


class AuthAPIClient(IAuthAPIClient):

    async def register(self, username: str, password: str) -> dict[str, Any]:
        response = await self.request(
            "POST", "users/create/", data={"username": username, "password": password}
        )
        return await response.json()

    async def login(self, username: str, password: str) -> dict[str, Any]:
        response = await self.request(
            "POST", "users/login/", data={"username": username, "password": password}
        )
        return await response.json()

    async def refresh_tokens(self, refresh_token: str) -> TokenRefreshResponse:
        response = await self.request(
            "POST", "users/refresh/", data={"refresh_token": refresh_token}
        )
        data = await response.json()
        return TokenRefreshResponse(**data)

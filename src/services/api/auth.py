from typing import Protocol, runtime_checkable

from src.models.auth import TokensResponse
from src.models.user import User
from src.services.api import BaseAPIClientProto, BaseAPIClient


@runtime_checkable
class AuthAPIClientProto(BaseAPIClientProto, Protocol):
    async def register(self, username: str, password: str) -> User: ...

    async def login(self, username: str, password: str) -> TokensResponse: ...

    async def refresh_tokens(self, refresh_token: str) -> TokensResponse: ...


class DefaultAuthAPIClient(BaseAPIClient):

    async def register(self, username: str, password: str) -> User:
        data = await self.request(
            "POST", "users/", data={"username": username, "password": password}
        )
        return User(**data)

    async def login(self, username: str, password: str) -> TokensResponse:
        data = await self.request(
            "POST", "users/login/", data={"username": username, "password": password}
        )
        return TokensResponse(**data)

    async def refresh_tokens(self, refresh_token: str) -> TokensResponse:
        data = await self.request(
            "POST", "users/refresh/", data={"refresh_token": refresh_token}
        )
        return TokensResponse(**data)

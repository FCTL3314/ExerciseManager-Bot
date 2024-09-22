from abc import ABC, abstractmethod
from typing import Any

from src.services.api.auth import IAuthAPIClient
from src.services.business.token_manager import ITokenManager


class IAuthService(ABC):
    @abstractmethod
    async def register(self, username: str, password: str) -> dict[str, Any]: ...

    @abstractmethod
    async def login(self, username: str, password: str) -> dict[str, Any]: ...

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> bool: ...


class AuthService:
    def __init__(
        self, api_client: IAuthAPIClient, token_manager: ITokenManager
    ) -> None:
        self._api_client = api_client
        self._token_manager = token_manager

    async def register(self, username: str, password: str) -> dict[str, Any]: ...

    async def login(self, username: str, password: str) -> dict[str, Any]: ...

    async def refresh_tokens(self, user_id: str) -> bool:
        refresh_token = await self._token_manager.get_refresh_token(user_id)

        if refresh_token is None:
            return False

        refresh_response = await self._api_client.refresh_tokens(refresh_token)
        await self._token_manager.save_tokens(
            user_id, refresh_response.access_token, refresh_response.refresh_token
        )
        return True

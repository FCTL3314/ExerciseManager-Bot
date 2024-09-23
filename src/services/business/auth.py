from abc import ABC, abstractmethod

from src.services.business.exceptions import PasswordsDoNotMatchError
from src.models.user import User
from src.services.api.auth import IAuthAPIClient
from src.services.business.token_manager import ITokenManager


class IAuthService(ABC):
    @abstractmethod
    async def register(self, username: str, password: str, retyped_password: str) -> User: ...

    @abstractmethod
    async def login(self, user_id: str, username: str, password: str) -> bool: ...

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> bool: ...


class AuthService(IAuthService):
    def __init__(
        self, api_client: IAuthAPIClient, token_manager: ITokenManager
    ) -> None:
        self._api_client = api_client
        self._token_manager = token_manager

    async def register(self, username: str, password: str, retyped_password: str) -> User:
        if retyped_password != password:
            raise PasswordsDoNotMatchError

        return await self._api_client.register(username, password)

    async def login(self, user_id: str, username: str, password: str) -> bool:
        tokens_response = await self._api_client.login(username, password)

        await self._token_manager.save_tokens(
            user_id, tokens_response.access_token, tokens_response.refresh_token
        )
        return True

    async def refresh_tokens(self, user_id: str) -> bool:
        refresh_token = await self._token_manager.get_refresh_token(user_id)

        if refresh_token is None:
            return False

        tokens_response = await self._api_client.refresh_tokens(refresh_token)
        await self._token_manager.save_tokens(
            user_id, tokens_response.access_token, tokens_response.refresh_token
        )
        return True

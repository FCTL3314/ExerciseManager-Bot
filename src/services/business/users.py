from abc import ABC, abstractmethod

from src.models.user import User
from src.services.api.users import IUserAPIClient
from src.services.business import BaseService, IAuthService
from src.services.business.token_manager import ITokenManager


class IUserService(BaseService, ABC):
    @abstractmethod
    async def me(self, *, user_id: int | str) -> User: ...


class UserService(IUserService):
    def __init__(
        self, auth_service: IAuthService, api_client: IUserAPIClient, token_manager: ITokenManager
    ) -> None:
        super().__init__(auth_service)
        self._api_client = api_client
        self._token_manager = token_manager

    @BaseService.refresh_tokens_on_unauthorized
    async def me(self, *, user_id: int | str) -> User:
        access_token = await self._token_manager.get_access_token(user_id)
        return await self._api_client.me(access_token)

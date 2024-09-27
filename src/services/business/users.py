from typing import runtime_checkable, Protocol

from src.models.user import User
from src.services.api.users import UserAPIClientProto
from src.services.business import BaseService, AuthServiceProto, BaseServiceProto
from src.services.business.token_manager import TokenManagerProto


@runtime_checkable
class UserServiceProto(BaseServiceProto, Protocol):
    async def me(self, user_id: int | str) -> User: ...


class DefaultUserService(BaseService):
    def __init__(
        self,
        auth_service: AuthServiceProto,
        api_client: UserAPIClientProto,
        token_manager: TokenManagerProto,
    ) -> None:
        super().__init__(auth_service)
        self._api_client = api_client
        self._token_manager = token_manager

    @BaseService.refresh_tokens_on_unauthorized
    async def me(self, user_id: int | str) -> User:
        access_token = await self._token_manager.get_access_token(user_id)
        return await self._api_client.me(access_token)

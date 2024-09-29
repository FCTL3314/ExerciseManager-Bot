from http import HTTPStatus
from typing import Protocol, runtime_checkable

from aiohttp import ClientResponseError

from src.database import KeyValueRepositoryProto
from src.models.user import User
from src.services.api.auth import AuthAPIClientProto
from src.services.api.users import UserAPIClientProto
from src.services.business.exceptions import PasswordsDoNotMatchError
from src.services.business.token_manager import TokenManagerProto


@runtime_checkable
class AuthServiceProto(Protocol):
    async def register(
        self, username: str, password: str, retyped_password: str
    ) -> User: ...

    async def login(self, user_id: int | str, username: str, password: str) -> bool: ...

    async def refresh_tokens(self, user_id: int | str) -> bool: ...

    async def get_user_id_by_tg_user_id(self, tg_user_id: int | str) -> str | None: ...


class DefaultAuthService:
    USER_ID_BY_TG_ID_KEY_TEMPLATE = "tg_user_id:__{tg_user_id}__user_id"

    def __init__(
        self,
        auth_api_client: AuthAPIClientProto,
        user_api_client: UserAPIClientProto,
        token_manager: TokenManagerProto,
        storage: KeyValueRepositoryProto,
    ) -> None:
        self._auth_api_client = auth_api_client
        self._user_api_client = user_api_client
        self._token_manager = token_manager
        self._storage = storage

    async def register(
        self, username: str, password: str, retyped_password: str
    ) -> User:
        if retyped_password != password:
            raise PasswordsDoNotMatchError

        return await self._auth_api_client.register(username, password)

    async def login(self, user_id: int | str, username: str, password: str) -> bool:
        try:
            tokens_response = await self._auth_api_client.login(username, password)
        except ClientResponseError as e:
            if e.status == HTTPStatus.UNAUTHORIZED:
                return False
            raise e

        await self._token_manager.save_tokens(
            user_id, tokens_response.access_token, tokens_response.refresh_token
        )

        me = await self._user_api_client.me(tokens_response.access_token)
        await self._storage.set(
            self.USER_ID_BY_TG_ID_KEY_TEMPLATE.format(tg_user_id=user_id), me.id
        )

        return True

    async def refresh_tokens(self, user_id: int | str) -> bool:
        refresh_token = await self._token_manager.get_refresh_token(user_id)

        if refresh_token is None:
            return False

        tokens_response = await self._auth_api_client.refresh_tokens(refresh_token)
        await self._token_manager.save_tokens(
            user_id, tokens_response.access_token, tokens_response.refresh_token
        )
        return True

    async def get_user_id_by_tg_user_id(self, tg_user_id: int | str) -> str | None:
        user_id = await self._storage.get(
            self.USER_ID_BY_TG_ID_KEY_TEMPLATE.format(tg_user_id=tg_user_id)
        )
        if user_id is None:
            return None
        return str(user_id)

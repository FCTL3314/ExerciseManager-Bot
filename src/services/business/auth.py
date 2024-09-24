from abc import ABC, abstractmethod
from http import HTTPStatus

from aiohttp import ClientResponseError

from src.database import IKeyValueRepository
from src.models.user import User
from src.services.api.auth import IAuthAPIClient
from src.services.api.users import IUserAPIClient
from src.services.business.exceptions import PasswordsDoNotMatchError
from src.services.business.token_manager import ITokenManager


class IAuthService(ABC):
    @abstractmethod
    async def register(
        self, *, username: int | str, password: str, retyped_password: str
    ) -> User: ...

    @abstractmethod
    async def login(
        self, *, user_id: int | str, username: str, password: str
    ) -> bool: ...

    @abstractmethod
    async def refresh_tokens(self, *, user_id: int | str) -> bool: ...

    @abstractmethod
    async def get_user_id_by_tg_user_id(
        self, *, user_id: int | str
    ) -> str | None: ...


class AuthService(IAuthService):
    USER_ID_BY_TG_ID_KEY_TEMPLATE = "tg_user_id:__{tg_user_id}__user_id"

    def __init__(
        self,
        auth_api_client: IAuthAPIClient,
        user_api_client: IUserAPIClient,
        token_manager: ITokenManager,
        storage: IKeyValueRepository,
    ) -> None:
        self._auth_api_client = auth_api_client
        self._user_api_client = user_api_client
        self._token_manager = token_manager
        self._storage = storage

    async def register(
        self, *, username: str, password: str, retyped_password: str
    ) -> User:
        if retyped_password != password:
            raise PasswordsDoNotMatchError

        return await self._auth_api_client.register(username, password)

    async def login(self, *, user_id: int | str, username: str, password: str) -> bool:
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

    async def refresh_tokens(self, *, user_id: int | str) -> bool:
        refresh_token = await self._token_manager.get_refresh_token(user_id)

        if refresh_token is None:
            return False

        tokens_response = await self._auth_api_client.refresh_tokens(refresh_token)
        await self._token_manager.save_tokens(
            user_id, tokens_response.access_token, tokens_response.refresh_token
        )
        return True

    async def get_user_id_by_tg_user_id(self, *, user_id: int | str) -> str | None:
        return str(
            await self._storage.get(
                self.USER_ID_BY_TG_ID_KEY_TEMPLATE.format(tg_user_id=user_id)
            )
        )

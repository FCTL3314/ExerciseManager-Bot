from abc import ABC, abstractmethod

from src.database import IKeyValueRepository
from src.services.business.enums import TokenType


class ITokenManager(ABC):

    @abstractmethod
    async def get_access_token(self, user_id: str | int) -> str | None: ...

    @abstractmethod
    async def get_refresh_token(self, user_id: str | int) -> str | None: ...

    @abstractmethod
    async def save_access_token(
        self, user_id: str | int, access_token: str
    ) -> None: ...

    @abstractmethod
    async def save_refresh_token(
        self, user_id: str | int, refresh_token: str
    ) -> None: ...

    @abstractmethod
    async def save_tokens(
        self, user_id: str | int, access_token: str, refresh_token: str
    ) -> None: ...


class TokenManager(ITokenManager):
    def __init__(
        self,
        storage: IKeyValueRepository,
        key_pattern: str = "user_{user_id}",
    ) -> None:
        self._storage = storage
        self._key_pattern = key_pattern

    async def _get_key(self, user_id: str | int, token_type: TokenType) -> str:
        key = self._key_pattern.format(user_id=user_id)
        if token_type.ACCESS:
            key += "__access_token"
        elif token_type.REFRESH:
            key += "__refresh_token"
        return key

    async def get_access_token(self, user_id: str | int) -> str | None:
        key = await self._get_key(user_id, TokenType.ACCESS)
        return await self._storage.get(key)

    async def get_refresh_token(self, user_id: str | int) -> str | None:
        key = await self._get_key(user_id, TokenType.REFRESH)
        return await self._storage.get(key)

    async def save_access_token(self, user_id: str | int, access_token: str) -> None:
        key = await self._get_key(user_id, TokenType.ACCESS)
        await self._storage.set(key, access_token)

    async def save_refresh_token(self, user_id: str | int, refresh_token: str) -> None:
        key = await self._get_key(user_id, TokenType.REFRESH)
        await self._storage.set(key, refresh_token)

    async def save_tokens(
        self, user_id: str | int, access_token: str, refresh_token: str
    ) -> None:
        await self.save_access_token(user_id, access_token)
        await self.save_refresh_token(user_id, refresh_token)

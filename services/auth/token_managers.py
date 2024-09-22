from abc import ABC, abstractmethod

from database import IKeyValueRepository
from database.types import KeyValueType
from services.auth.enums import TokenType


class ITokenManager(ABC):

    @abstractmethod
    async def save(self, user_id: str | int, token: str, token_type: TokenType) -> None: ...

    @abstractmethod
    async def get(self, user_id: str | int, token_type: TokenType) -> KeyValueType: ...


class TokenManager(ITokenManager):
    def __init__(
        self,
        storage: IKeyValueRepository,
        key_pattern: str = "user_{user_id}",
    ) -> None:
        self._storage = storage
        self._key_pattern = key_pattern

    async def _generate_key(self, user_id: str | int, token_type: TokenType) -> str:
        key = self._key_pattern.format(user_id=user_id)
        if token_type.ACCESS:
            key += "__access_token"
        elif token_type.REFRESH:
            key += "__refresh_token"
        return key

    async def save(self, user_id: str | int, token: str, token_type: TokenType) -> None:
        key = await self._generate_key(user_id, token_type)
        await self._storage.set(key, token)

    async def get(self, user_id: str | int, token_type: TokenType) -> str:
        key = await self._generate_key(user_id, token_type)
        return await self._storage.get(key)

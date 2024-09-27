from typing import Protocol

from src.database.types import KeyValueType


class KeyValueRepositoryProto(Protocol):
    async def get(self, key: str) -> KeyValueType: ...

    async def set(
        self, key: str, value: KeyValueType, expire: int | None = None
    ) -> None: ...

    async def delete(self, key: str) -> None: ...

    async def exists(self, key: str) -> bool: ...

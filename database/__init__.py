from abc import ABC, abstractmethod

from database.types import KeyValueType


class IKeyValueRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> KeyValueType: ...

    @abstractmethod
    async def set(self, key: str, value: KeyValueType, expire: int | None = None) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def exists(self, key: str) -> bool: ...

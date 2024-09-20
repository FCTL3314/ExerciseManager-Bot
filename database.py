from abc import ABC, abstractmethod

import redis

type KeyValueType = str | int | float | bool | bytes | None


class IKeyValueRepository(ABC):
    @abstractmethod
    def get(self, key: str) -> KeyValueType: ...

    @abstractmethod
    def set(self, key: str, value: KeyValueType, expire: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def exists(self, key: str) -> bool: ...


class RedisRepository(IKeyValueRepository):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0) -> None:
        self._client = redis.Redis(host=host, port=port, db=db)

    async def get(self, key: str) -> KeyValueType:
        value = await self._client.get(key)
        if value is not None:
            try:
                return value.decode('utf-8')
            except AttributeError:
                return value
        return None

    async def set(self, key: str, value: KeyValueType, expire: int | None = None) -> None:
        if isinstance(value, (str, bytes)):
            await self._client.set(key, value, ex=expire)
        else:
            await self._client.set(key, str(value), ex=expire)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self._client.exists(key) > 0

from abc import ABC, abstractmethod

from redis.asyncio import Redis

type KeyValueType = str | int | float | bool | bytes | None


class IKeyValueRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> KeyValueType: ...

    @abstractmethod
    async def set(self, key: str, value: KeyValueType, expire: int | None = None) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def exists(self, key: str) -> bool: ...


class RedisRepository(IKeyValueRepository):
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self._client = Redis(host=host, port=port, db=db)

    async def get(self, key: str) -> KeyValueType:
        value = await self._client.get(key)
        if value is None:
            return None
        try:
            return value.decode("utf-8")
        except AttributeError:
            return value

    async def set(self, key: str, value: KeyValueType, expire: int | None = None) -> None:
        if isinstance(value, (str, bytes)):
            await self._client.set(key, value, ex=expire)
        else:
            await self._client.set(key, str(value), ex=expire)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self._client.exists(key) > 0

from abc import ABC, abstractmethod
from typing import Any


class IAPIClient(ABC):

    @abstractmethod
    async def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] = None,
        params: dict[str, Any] = None,
    ) -> dict[str, Any]: ...

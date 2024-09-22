from abc import ABC
from typing import Any


class IExerciseManagerAPIClient(ABC):
    async def refresh_tokens(self) -> None: ...

    async def get_users(self) -> None: ...


class ExerciseManagerAPIClient(IExerciseManagerAPIClient):

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] = None,
        params: dict[str, Any] = None,
    ) -> dict[str, Any]: ...

    async def refresh_tokens(self): ...

    async def get_users(self): ...

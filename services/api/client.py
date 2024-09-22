from typing import Any

from services.api import IAPIClient


class ExerciseManagerAPIClient(IAPIClient):

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] = None,
        params: dict[str, Any] = None,
    ) -> dict[str, Any]:
        ...

    async def refresh_tokens(self): ...

    async def get_users(self): ...

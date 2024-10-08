from http import HTTPStatus
from typing import Any, Protocol, runtime_checkable
from urllib.parse import urljoin

from aiogram.client.session import aiohttp


@runtime_checkable
class BaseAPIClientProto(Protocol):

    async def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any: ...

    async def get_auth_header(self, access_token: str) -> dict[str, Any]: ...


class BaseAPIClient:
    def __init__(
        self, base_url: str, session: aiohttp.ClientSession | None = None
    ) -> None:
        self._base_url = base_url
        self._session = session or aiohttp.ClientSession()

    async def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        url = urljoin(self._base_url, endpoint)
        async with self._session.request(
            method,
            url,
            json=data,
            params=params,
            headers=headers,
        ) as response:
            status = HTTPStatus(response.status)
            if status.is_success:
                return await response.json()
            response.raise_for_status()

    @staticmethod
    async def get_auth_header(access_token: str) -> dict[str, Any]:
        return {"Authorization": f"Bearer {access_token}"}

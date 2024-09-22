from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Callable
from urllib.parse import urljoin

from aiogram.client.session import aiohttp

from services.auth.enums import TokenType
from services.auth.token_managers import ITokenManager


class IExerciseManagerAPIClient(ABC):
    @abstractmethod
    async def set_current_tg_user_id(self, _id: int | str) -> None: ...

    @abstractmethod
    async def set_callback_on_unauthorized(self, callback: Callable[[str | int], None]) -> None: ...

    @abstractmethod
    async def refresh_tokens(self) -> bool: ...

    @abstractmethod
    async def get_user(self, _id: int) -> dict[str, Any]: ...

    @abstractmethod
    async def get_users(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def get_workout(self, _id: int) -> dict[str, Any]: ...

    @abstractmethod
    async def get_workouts(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def get_exercise(self, _id: int) -> dict[str, Any]: ...

    @abstractmethod
    async def get_exercises(self) -> list[dict[str, Any]]: ...


class ExerciseManagerAPIClient(IExerciseManagerAPIClient):

    def __init__(
        self,
        base_url: str,
        token_manager: ITokenManager,
        callback_on_unauthorized: Callable[[str | int], None] | None = None,
    ) -> None:
        self._base_url = base_url
        self._token_manager = token_manager
        self._current_tg_user_id: int | str | None = None
        self._callback_on_unauthorized = callback_on_unauthorized

    async def set_current_tg_user_id(self, _id: int | str) -> None:
        self._current_tg_user_id = _id

    async def set_callback_on_unauthorized(self, callback: Callable[[str | int], None]) -> None:
        self._callback_on_unauthorized = callback

    async def get_url(self, endpoint: str) -> str:
        return urljoin(self._base_url, endpoint)

    async def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] = None,
        params: dict[str, Any] = None,
        refresh_token_on_unauthorized: bool = True,
    ) -> Any:
        async with aiohttp.ClientSession() as session:
            url = await self.get_url(endpoint)
            response = await session.request(method, url, json=data, params=params)

            if response.status == HTTPStatus.UNAUTHORIZED:

                if not refresh_token_on_unauthorized:
                    if self._callback_on_unauthorized is None:
                        return
                    return self._callback_on_unauthorized(self._current_tg_user_id)


                is_refreshed = await self.refresh_tokens()
                if is_refreshed:
                    return await self.request(
                        method, endpoint, data, params, refresh_token_on_unauthorized=False
                    )

            return await response.json()

    async def refresh_tokens(self) -> bool:
        refresh_token = await self._token_manager.get(
            self._current_tg_user_id, TokenType.REFRESH
        )

        if refresh_token is None:
            return False

        async with aiohttp.ClientSession() as session:
            url = await self.get_url("users/refresh/")
            response = await session.post(
                url,
                json={"refresh_token": refresh_token},
            )
            if response.status != HTTPStatus.OK:
                return False

            data = await response.json()
            new_access_token = data.get("access_token")
            new_refresh_token = data.get("refresh_token")
            await self._token_manager.save(
                self._current_tg_user_id, new_access_token, TokenType.ACCESS
            )
            await self._token_manager.save(
                self._current_tg_user_id, new_refresh_token, TokenType.REFRESH
            )
            return True

    async def get_user(self, _id: int) -> dict[str, Any]:
        return await self.request("GET", f"users/{_id}/")

    async def get_users(self) -> list[dict[str, Any]]:
        return await self.request("GET", f"users/")

    async def get_workout(self, _id: int) -> dict[str, Any]:
        return await self.request("GET", f"workouts/{_id}/")

    async def get_workouts(self) -> list[dict[str, Any]]:
        return await self.request("GET", f"workouts/")

    async def get_exercise(self, _id: int) -> dict[str, Any]:
        return await self.request("GET", f"exercises/{_id}/")

    async def get_exercises(self) -> list[dict[str, Any]]:
        return await self.request("GET", f"exercises/")

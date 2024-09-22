from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any
from urllib.parse import urljoin

from aiogram.client.session import aiohttp

from services.auth.enums import TokenType
from services.auth.token_managers import ITokenManager


class IExerciseManagerAPIClient(ABC):
    @abstractmethod
    async def set_current_tg_user_id(self, _id: int | str) -> None: ...

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
    ) -> None:
        self._base_url = base_url
        self._token_manager = token_manager
        self._current_tg_user_id: int | str | None = None

    async def set_current_tg_user_id(self, _id: int | str) -> None:
        self._current_tg_user_id = _id

    async def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] = None,
        params: dict[str, Any] = None,
        process_unauthorized: bool = True,
    ) -> Any:
        url = urljoin(self._base_url, endpoint)
        async with aiohttp.ClientSession() as session:
            response = await session.request(method, url, json=data, params=params)
            if response.status == HTTPStatus.UNAUTHORIZED and process_unauthorized:
                await self.refresh_tokens()
                return await self.request(
                    method, endpoint, data, params, process_unauthorized=False
                )
            return await response.json()

    async def refresh_tokens(self) -> bool:
        refresh_token = await self._token_manager.get(
            self._current_tg_user_id, TokenType.REFRESH
        )

        if refresh_token is None:
            return False

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                f"{self._base_url}/auth/refresh/",
                json={"refresh_token": refresh_token},
            )
            if response.status == HTTPStatus.OK:
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
            return False

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

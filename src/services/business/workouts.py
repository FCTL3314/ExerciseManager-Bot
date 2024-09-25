from abc import ABC, abstractmethod

from src.models.workout import Workout
from src.services.api.workouts import IWorkoutAPIClient
from src.services.business import BaseService, IAuthService
from src.services.business.token_manager import ITokenManager


class IWorkoutService(BaseService, ABC):
    @abstractmethod
    async def list(self, *, user_id: int | str | None) -> list[Workout]: ...

    @abstractmethod
    async def create(
        self, *, user_id: int | str, name: str, description: str
    ) -> Workout: ...


class WorkoutService(IWorkoutService):
    def __init__(
        self,
        auth_service: IAuthService,
        api_client: IWorkoutAPIClient,
        token_manager: ITokenManager,
    ) -> None:
        super().__init__(auth_service)
        self._api_client = api_client
        self._token_manager = token_manager

    async def list(self, *, user_id: int | str | None) -> list[Workout]:
        api_user_id = await self._auth_service.get_user_id_by_tg_user_id(user_id=user_id)
        return await self._api_client.list(user_id=api_user_id)

    @BaseService.refresh_tokens_on_unauthorized
    async def create(
        self, *, user_id: int | str, name: str, description: str
    ) -> Workout:
        access_token = await self._token_manager.get_access_token(user_id)
        return await self._api_client.create(access_token, name, description)

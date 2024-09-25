from abc import ABC, abstractmethod

from src.models.workout import Workout
from src.services.api.workouts import IWorkoutAPIClient
from src.services.business import BaseService, IAuthService
from src.services.business.token_manager import ITokenManager


class IWorkoutService(BaseService, ABC):
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

    @BaseService.refresh_tokens_on_unauthorized
    async def create(
        self, *, user_id: int | str, name: str, description: str
    ) -> Workout:
        access_token = await self._token_manager.get_access_token(user_id)
        return await self._api_client.create(access_token, name, description)

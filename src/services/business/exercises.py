from datetime import timedelta
from typing import runtime_checkable, Protocol

from src.models.exercise import Exercise
from src.services.api.exercises import ExerciseAPIClientProto
from src.services.business import BaseService, AuthServiceProto, BaseServiceProto
from src.services.business.token_manager import TokenManagerProto
from src.services.duration import to_nanoseconds


@runtime_checkable
class ExerciseServiceProto(BaseServiceProto, Protocol):
    async def create(
        self, user_id: int | str, name: str, description: str, duration: timedelta
    ) -> Exercise: ...


class DefaultExerciseService(BaseService):
    def __init__(
        self,
        auth_service: AuthServiceProto,
        api_client: ExerciseAPIClientProto,
        token_manager: TokenManagerProto,
    ) -> None:
        super().__init__(auth_service)
        self._api_client = api_client
        self._token_manager = token_manager

    @BaseService.refresh_tokens_on_unauthorized
    async def create(
        self, user_id: int | str, name: str, description: str, duration: timedelta
    ) -> Exercise:
        access_token = await self._token_manager.get_access_token(user_id)
        _duration = await to_nanoseconds(duration)
        return await self._api_client.create(access_token, name, description, _duration)

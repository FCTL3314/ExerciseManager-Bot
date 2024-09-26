from abc import ABC, abstractmethod

from src.config.types import ExerciseValidationSettings
from src.models.workout import Workout
from src.services.api.exercises import IExerciseAPIClient
from src.services.api.workouts import IWorkoutAPIClient
from src.services.business import BaseService, IAuthService
from src.services.business.token_manager import ITokenManager
from src.services.duration import to_nanoseconds, parse_duration_string
from src.services.exceptions import ExerciseBreakTooLongError


class IWorkoutService(BaseService, ABC):
    @abstractmethod
    async def list(self, *, user_id: int | str | None) -> list[Workout]: ...

    @abstractmethod
    async def create(
        self, *, user_id: int | str, name: str, description: str
    ) -> Workout: ...

    @abstractmethod
    async def add_exercise(
        self,
        *,
        user_id: int | str,
        workout_id: int | str,
        name: str,
        description: str,
        duration: str,
        break_time: str,
    ) -> Workout: ...


class DefaultWorkoutService(IWorkoutService):
    def __init__(
        self,
        auth_service: IAuthService,
        workout_api_client: IWorkoutAPIClient,
        exercise_api_client: IExerciseAPIClient,
        token_manager: ITokenManager,
        validation_settings: ExerciseValidationSettings,
    ) -> None:
        super().__init__(auth_service)
        self._workout_api_client = workout_api_client
        self._exercise_api_client = exercise_api_client
        self._token_manager = token_manager
        self._validation_settings = validation_settings

    async def list(self, *, user_id: int | str | None) -> list[Workout]:
        api_user_id = await self._auth_service.get_user_id_by_tg_user_id(
            user_id=user_id
        )
        return await self._workout_api_client.list(user_id=api_user_id)

    @BaseService.refresh_tokens_on_unauthorized
    async def create(
        self, *, user_id: int | str, name: str, description: str
    ) -> Workout:
        access_token = await self._token_manager.get_access_token(user_id)
        return await self._workout_api_client.create(access_token, name, description)

    @BaseService.refresh_tokens_on_unauthorized
    async def add_exercise(
        self,
        *,
        user_id: int | str,
        workout_id: int | str,
        name: str,
        description: str,
        duration: str,
        break_time: str,
    ) -> Workout:
        access_token = await self._token_manager.get_access_token(user_id)

        _duration = parse_duration_string(duration)
        _break_time = parse_duration_string(break_time)

        if _break_time > self._validation_settings.max_exercise_break_time:
            raise ExerciseBreakTooLongError

        exercise = await self._exercise_api_client.create(
            access_token, name, description, to_nanoseconds(_duration),
        )
        return await self._workout_api_client.add_exercise(
            access_token, workout_id, exercise.id, to_nanoseconds(_break_time)
        )

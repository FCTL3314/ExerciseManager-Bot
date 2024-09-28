import base64
import pickle
from typing import runtime_checkable, Protocol, Any

from src.config.types import ExerciseValidationSettings
from src.database import KeyValueRepositoryProto
from src.models.workout import (
    Workout,
    WorkoutPaginatedResponse,
    WorkoutSettings,
    WorkoutState,
    SerializedWorkoutState,
)
from src.services.api.exercises import ExerciseAPIClientProto
from src.services.api.workouts import WorkoutAPIClientProto
from src.services.business import BaseService, AuthServiceProto, BaseServiceProto
from src.services.business.token_manager import TokenManagerProto
from src.services.duration import ato_nanoseconds, parse_duration_string
from src.services.exceptions import (
    ExerciseBreakTooLongError,
    ExerciseDurationTooLongError,
)


@runtime_checkable
class WorkoutServiceProto(BaseServiceProto, Protocol):
    async def retrieve(self, workout_id: str | int) -> Workout: ...

    async def list(
        self,
        user_id: int | str | None,
        limit: int = 64,
        offset: int = 0,
    ) -> WorkoutPaginatedResponse: ...

    async def create(
        self, user_id: int | str, name: str, description: str
    ) -> Workout: ...

    async def add_exercise(
        self,
        user_id: int | str,
        workout_id: int | str,
        name: str,
        description: str,
        duration: str,
        break_time: str,
    ) -> Workout: ...

    async def get_workout_settings(self, data: dict[str, Any]) -> WorkoutSettings: ...

    async def create_serialized_workout_state(
        self, workout: Workout
    ) -> SerializedWorkoutState: ...

    async def get_current_workout_state(self, data: dict[str, Any]) -> WorkoutState: ...

    async def get_break_seconds(
        self, workout_state: WorkoutState, workout_settings: WorkoutSettings
    ) -> int: ...


class DefaultWorkoutService(BaseService):
    def __init__(
        self,
        auth_service: AuthServiceProto,
        workout_api_client: WorkoutAPIClientProto,
        exercise_api_client: ExerciseAPIClientProto,
        token_manager: TokenManagerProto,
        storage: KeyValueRepositoryProto,
        validation_settings: ExerciseValidationSettings,
    ) -> None:
        super().__init__(auth_service)
        self._workout_api_client = workout_api_client
        self._exercise_api_client = exercise_api_client
        self._token_manager = token_manager
        self._storage = storage
        self._validation_settings = validation_settings

    async def retrieve(self, workout_id: str | int) -> Workout:
        return await self._workout_api_client.retrieve(workout_id=workout_id)

    async def list(
        self,
        user_id: int | str | None,
        limit: int = 64,
        offset: int = 0,
    ) -> WorkoutPaginatedResponse:
        api_user_id = await self._auth_service.get_user_id_by_tg_user_id(
            user_id=user_id
        )
        return await self._workout_api_client.list(
            user_id=api_user_id, limit=limit, offset=offset
        )

    @BaseService.refresh_tokens_on_unauthorized
    async def create(self, user_id: int | str, name: str, description: str) -> Workout:
        access_token = await self._token_manager.get_access_token(user_id)
        return await self._workout_api_client.create(access_token, name, description)

    @BaseService.refresh_tokens_on_unauthorized
    async def add_exercise(
        self,
        user_id: int | str,
        workout_id: int | str,
        name: str,
        description: str,
        duration: str,
        break_time: str,
    ) -> Workout:
        access_token = await self._token_manager.get_access_token(user_id)

        _duration = await parse_duration_string(duration)
        _break_time = await parse_duration_string(break_time)

        if _duration > self._validation_settings.max_exercise_duration:
            raise ExerciseDurationTooLongError

        if _break_time > self._validation_settings.max_exercise_break_time:
            raise ExerciseBreakTooLongError

        exercise = await self._exercise_api_client.create(
            access_token,
            name,
            description,
            await ato_nanoseconds(_duration),
        )
        return await self._workout_api_client.add_exercise(
            access_token, workout_id, exercise.id, await ato_nanoseconds(_break_time)
        )

    async def get_workout_settings(self, data: dict[str, Any]) -> WorkoutSettings:
        try:
            pre_start_timer_seconds = int(
                await self._storage.get("pre_start_timer_seconds")
            )
        except TypeError:
            pre_start_timer_seconds = 15  # TODO:  Remove hardcode
        manual_mode_enabled = data.get("manual_mode_enabled", False)

        return WorkoutSettings(
            pre_start_timer_seconds=pre_start_timer_seconds,
            manual_mode_enabled=manual_mode_enabled,
        )

    @staticmethod
    async def create_serialized_workout_state(
        workout: Workout,
    ) -> SerializedWorkoutState:
        serialized_workout_exercises = base64.b64encode(
            pickle.dumps(workout.workout_exercises)
        ).decode("utf-8")

        return SerializedWorkoutState(
            workout_exercises=serialized_workout_exercises,
            current_workout_exercise_index=0,
        )

    @staticmethod
    async def get_current_workout_state(data: dict[str, Any]) -> WorkoutState:
        current_workout_exercise_index = data.get("current_workout_exercise_index", 0)
        workout_exercises = pickle.loads(base64.b64decode(data["workout_exercises"]))
        current_workout_exercise = workout_exercises[current_workout_exercise_index]

        return WorkoutState(
            workout_exercises=workout_exercises,
            current_workout_exercise=current_workout_exercise,
        )

    @staticmethod
    async def get_break_seconds(
        workout_state: WorkoutState, workout_settings: WorkoutSettings
    ) -> int:
        return (
            workout_settings.pre_start_timer_seconds
            if workout_state.is_first_exercise
            else int(workout_state.current_workout_exercise.break_time.total_seconds())
        )

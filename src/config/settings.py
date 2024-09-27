from decouple import RepositoryEnv, Config

from src.config import SettingsLoaderProto, Settings
from src.config.types import (
    LoggingSettings,
    ValidationSettings,
    UserValidationSettings,
    LocalizationSettings,
    WorkoutValidationSettings,
    ExerciseValidationSettings,
    PaginationSettings,
    WorkoutPaginationSettings,
)
from src.services.duration import from_nanoseconds


class SettingsLoader(SettingsLoaderProto):

    def __init__(self) -> None:
        self._config = Config(RepositoryEnv("settings.ini"))

    async def _load_logging(self) -> LoggingSettings:
        return LoggingSettings(
            format=self._config("LOGGING_FORMAT"),
        )

    async def _load_validation(self) -> ValidationSettings:
        user_validation = UserValidationSettings(
            username_max_length=self._config("USER_USERNAME_MAX_LENGTH", cast=int),
            username_min_length=self._config("USER_USERNAME_MIN_LENGTH", cast=int),
            password_max_length=self._config("USER_PASSWORD_MAX_LENGTH", cast=int),
            password_min_length=self._config("USER_PASSWORD_MIN_LENGTH", cast=int),
        )
        workout_validation = WorkoutValidationSettings(
            name_max_length=self._config("WORKOUT_NAME_MAX_LENGTH", cast=int),
            name_min_length=self._config("WORKOUT_NAME_MIN_LENGTH", cast=int),
        )
        exercise_validation = ExerciseValidationSettings(
            name_max_length=self._config("EXERCISE_NAME_MAX_LENGTH", cast=int),
            name_min_length=self._config("EXERCISE_NAME_MIN_LENGTH", cast=int),
            max_exercise_duration=await from_nanoseconds(
                self._config("MAX_EXERCISE_DURATION", cast=int)
            ),
            max_exercise_break_time=await from_nanoseconds(
                self._config("MAX_EXERCISE_BREAK_TIME", cast=int)
            ),
        )

        return ValidationSettings(
            user=user_validation,
            workout=workout_validation,
            exercise=exercise_validation,
        )

    async def _load_pagination(self) -> PaginationSettings:
        workout_pagination = WorkoutPaginationSettings(
            workouts_keyboard_paginate_by=self._config(
                "WORKOUTS_KEYBOARD_PAGINATE_BY", cast=int
            ),
            workouts_keyboard_buttons_per_row=self._config(
                "WORKOUT_KEYBOARD_BUTTONS_PER_ROW", cast=int
            ),
        )

        return PaginationSettings(
            workout=workout_pagination,
        )

    async def _load_localization(self) -> LocalizationSettings:
        return LocalizationSettings(
            locales_path=self._config("LOCALIZATION_LOCALES_PATH"),
            default_locale=self._config("LOCALIZATION_DEFAULT_LOCALE"),
            domain=self._config("LOCALIZATION_DOMAIN"),
        )

    async def load(self) -> Settings:
        logging = await self._load_logging()
        validation = await self._load_validation()
        pagination = await self._load_pagination()
        localization = await self._load_localization()

        return Settings(
            logging=logging,
            validation=validation,
            pagination=pagination,
            localization=localization,
        )

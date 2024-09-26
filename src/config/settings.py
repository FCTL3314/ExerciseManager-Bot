from decouple import RepositoryEnv, Config

from src.config import ISettingsLoader, Settings
from src.config.types import (
    LoggingSettings,
    ValidationSettings,
    UserValidationSettings,
    LocalizationSettings,
    WorkoutValidationSettings,
    ExerciseValidationSettings,
)
from src.services.duration import from_nanoseconds


class SettingsLoader(ISettingsLoader):

    def __init__(self) -> None:
        self._config = Config(RepositoryEnv("settings.ini"))

    def _load_logging(self) -> LoggingSettings:
        return LoggingSettings(
            format=self._config("LOGGING_FORMAT"),
        )

    def _load_validation(self) -> ValidationSettings:
        user_validation_config = UserValidationSettings(
            username_max_length=self._config("USER_USERNAME_MAX_LENGTH", cast=int),
            username_min_length=self._config("USER_USERNAME_MIN_LENGTH", cast=int),
            password_max_length=self._config("USER_PASSWORD_MAX_LENGTH", cast=int),
            password_min_length=self._config("USER_PASSWORD_MIN_LENGTH", cast=int),
        )
        workout_validation_config = WorkoutValidationSettings(
            name_max_length=self._config("WORKOUT_NAME_MAX_LENGTH", cast=int),
            name_min_length=self._config("WORKOUT_NAME_MIN_LENGTH", cast=int),
        )
        exercise_validation_config = ExerciseValidationSettings(
            name_max_length=self._config("EXERCISE_NAME_MAX_LENGTH", cast=int),
            name_min_length=self._config("EXERCISE_NAME_MIN_LENGTH", cast=int),
            max_exercise_duration=from_nanoseconds(
                self._config("MAX_EXERCISE_DURATION", cast=int)
            ),
            max_exercise_break_time=from_nanoseconds(
                self._config("MAX_EXERCISE_BREAK_TIME", cast=int)
            ),
        )

        return ValidationSettings(
            user=user_validation_config,
            workout=workout_validation_config,
            exercise=exercise_validation_config,
        )

    def _load_localization(self) -> LocalizationSettings:
        return LocalizationSettings(
            locales_path=self._config("LOCALIZATION_LOCALES_PATH"),
            default_locale=self._config("LOCALIZATION_DEFAULT_LOCALE"),
            domain=self._config("LOCALIZATION_DOMAIN"),
        )

    def load(self) -> Settings:
        logging = self._load_logging()
        validation = self._load_validation()
        localization = self._load_localization()
        return Settings(
            logging=logging,
            validation=validation,
            localization=localization,
        )

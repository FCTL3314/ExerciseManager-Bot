from decouple import RepositoryEnv, Config

from config import ISettingsLoader, Settings
from config.types import LoggingSettings, ValidationSettings, UserValidationConfig


class SettingsLoader(ISettingsLoader):

    def __init__(self) -> None:
        self._config = Config(RepositoryEnv("settings.ini"))

    def _load_logging(self) -> LoggingSettings:
        return LoggingSettings(
            format=self._config("LOGGING_FORMAT"),
        )

    def _load_validation(self) -> ValidationSettings:
        user_validation_config = UserValidationConfig(
            username_max_length=self._config("USERNAME_MAX_LENGTH", cast=int),
            username_min_length=self._config("USERNAME_MIN_LENGTH", cast=int),
            password_max_length=self._config("PASSWORD_MAX_LENGTH", cast=int),
            password_min_length=self._config("PASSWORD_MIN_LENGTH", cast=int),
        )

        return ValidationSettings(
            user=user_validation_config,
        )

    def load(self) -> Settings:
        logging = self._load_logging()
        validation = self._load_validation()
        return Settings(
            logging=logging,
            validation=validation,
        )

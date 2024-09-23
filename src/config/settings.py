from decouple import RepositoryEnv, Config

from src.config import ISettingsLoader, Settings
from src.config.types import (
    LoggingSettings,
    ValidationSettings,
    UserValidationConfig,
    LocalizationSettings,
)


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

    def _load_localization(self) -> LocalizationSettings:
        return LocalizationSettings(
            locales_path=self._config("LOCALIZATION_LOCALES_PATH"),
            default_locale=self._config("LOCALIZATION_DEFAULT_LOCALE"),
            domain=self._config("LOCALIZATION_DOMAIN")
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

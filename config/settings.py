from decouple import RepositoryEnv, Config

from config import ISettingsLoader, Settings
from config.types import Logging


class SettingsLoader(ISettingsLoader):

    def __init__(self) -> None:
        self._config = Config(RepositoryEnv("settings.ini"))

    def _load_logging(self) -> Logging:
        return Logging(
            format=self._config("LOGGING_FORMAT"),
        )

    def load(self) -> Settings:
        logging = self._load_logging()
        return Settings(
            logging=logging,
        )

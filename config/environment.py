import os
from abc import abstractmethod, ABC

from dotenv import load_dotenv

from config.types import BotConfig, EnvironmentConfig


class IEnvironmentConfigLoader(ABC):

    @abstractmethod
    def load(self) -> EnvironmentConfig: ...


class EnvironmentConfigLoader:
    def __init__(self) -> None:
        load_dotenv()

    @staticmethod
    def _load_bot_config() -> BotConfig:
        return BotConfig(
            token=os.getenv("BOT_TOKEN"),
        )

    def load(self) -> EnvironmentConfig:
        bot_config = self._load_bot_config()
        return EnvironmentConfig(
            bot=bot_config,
        )

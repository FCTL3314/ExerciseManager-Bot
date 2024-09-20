import os
from abc import abstractmethod, ABC

from dotenv import load_dotenv

from config.exceptions import RedisPortIsNotDigit
from config.types import BotConfig, EnvironmentConfig, RedisConfig


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

    @staticmethod
    def _load_redis_config() -> RedisConfig:
        if not (port := os.getenv("REDIS_PORT")).isdigit():
            raise RedisPortIsNotDigit

        return RedisConfig(
            host=os.getenv("REDIS_HOST"),
            port=int(port),
        )

    def load(self) -> EnvironmentConfig:
        bot_config = self._load_bot_config()
        redis_config = self._load_redis_config()
        return EnvironmentConfig(
            bot=bot_config,
            redis=redis_config,
        )

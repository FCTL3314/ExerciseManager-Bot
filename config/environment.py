from decouple import config

from config import IEnvironmentConfigLoader
from config.types import BotConfig, EnvironmentConfig, RedisConfig


class EnvironmentConfigLoader(IEnvironmentConfigLoader):
    def __init__(self, search_path: str = "./") -> None:
        config.search_path = search_path

    @staticmethod
    def _load_bot_config() -> BotConfig:
        return BotConfig(
            token=config("BOT_TOKEN"),
        )

    @staticmethod
    def _load_redis_config() -> RedisConfig:
        return RedisConfig(
            host=config("REDIS_HOST"),
            port=config("REDIS_PORT", cast=int),
        )

    def load(self) -> EnvironmentConfig:
        bot_config = self._load_bot_config()
        redis_config = self._load_redis_config()
        return EnvironmentConfig(
            bot=bot_config,
            redis=redis_config,
        )

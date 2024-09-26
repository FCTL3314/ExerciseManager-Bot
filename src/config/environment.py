from decouple import RepositoryEnv, Config

from src.config import IEnvironmentConfigLoader
from src.config.types import BotConfig, EnvironmentConfig, RedisConfig, APIConfig


class EnvironmentConfigLoader(IEnvironmentConfigLoader):
    def __init__(self) -> None:
        self._config = Config(RepositoryEnv(".env"))

    async def _load_bot_config(self) -> BotConfig:
        return BotConfig(
            token=self._config("BOT_TOKEN"),
        )

    async def _load_api_config(self) -> APIConfig:
        return APIConfig(
            base_url=self._config("API_BASE_URL"),
        )

    async def _load_redis_config(self) -> RedisConfig:
        return RedisConfig(
            host=self._config("REDIS_HOST"),
            port=self._config("REDIS_PORT", cast=int),
        )

    async def load(self) -> EnvironmentConfig:
        bot_config = await self._load_bot_config()
        api_config = await self._load_api_config()
        redis_config = await self._load_redis_config()
        return EnvironmentConfig(
            bot=bot_config,
            api=api_config,
            redis=redis_config,
        )

from decouple import RepositoryEnv, Config

from src.config.types import BotConfig, EnvironmentConfig, RedisConfig, APIConfig


class EnvironmentConfigLoader:
    def __init__(self) -> None:
        self._config = Config(RepositoryEnv(".env"))

    async def _load_bot_config(self) -> BotConfig:
        use_webhook = self._config("USE_WEBHOOK", cast=bool)
        webhook_host = self._config("WEBHOOK_HOST")
        webhook_secret = self._config("WEBHOOK_SECRET")

        if use_webhook and not all((webhook_host, webhook_secret)):
            raise ValueError(
                "WEBHOOK_HOST, WEBHOOK_PATH, and WEBHOOK_SECRET environment "
                "variables are required when using webhook."
            )

        return BotConfig(
            token=self._config("BOT_TOKEN"),
            use_webhook=use_webhook,
            webhook_host=webhook_host,
            webhook_secret=webhook_secret,
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

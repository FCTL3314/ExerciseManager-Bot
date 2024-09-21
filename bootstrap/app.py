from bootstrap.types import App
from bot.loader import BotLoader, IBotLoader
from bot.types import Bot
from config import ConfigLoader
from config.environment import EnvironmentConfigLoader
from config.settings import SettingsLoader
from config.types import Config
from database import IKeyValueRepository
from database.redis import RedisRepository


class Bootstrap:

    @staticmethod
    def _init_config() -> Config:
        loader = ConfigLoader(
            env_loader=EnvironmentConfigLoader(),
            settings_loader=SettingsLoader(),
        )
        return loader.load()

    @staticmethod
    def _init_storage(host: str, port: int) -> IKeyValueRepository:
        return RedisRepository(host=host, port=port, db=0)

    @staticmethod
    def _init_bot(config: Config) -> Bot:
        bot_loader: IBotLoader = BotLoader(config=config)
        return bot_loader.load()

    def initialize_app(self) -> App:
        config = self._init_config()
        storage = self._init_storage(
            host=config.env.redis.host,
            port=config.env.redis.port,
        )
        bot = self._init_bot(config)
        return App(
            config=config,
            storage=storage,
            bot=bot,
        )

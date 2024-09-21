from bootstrap.types import App
from bot.loader import initialize_bot
from config import ConfigLoader
from config.types import Config
from config.environment import EnvironmentConfigLoader
from config.settings import SettingsLoader
from database import IKeyValueRepository
from database.redis import RedisRepository


class Bootstrap:

    @staticmethod
    def _load_config() -> Config:
        loader = ConfigLoader(
            env_loader=EnvironmentConfigLoader(),
            settings_loader=SettingsLoader(),
        )
        return loader.load()

    @staticmethod
    def initialize_storage(host: str, port: int) -> IKeyValueRepository:
        return RedisRepository(host=host, port=port, db=0)

    def initialize_app(self) -> App:
        config = self._load_config()
        storage = self.initialize_storage(
            host=config.env.redis.host,
            port=config.env.redis.port,
        )
        bot = initialize_bot(config=config)
        return App(
            config=config,
            storage=storage,
            bot=bot,
        )

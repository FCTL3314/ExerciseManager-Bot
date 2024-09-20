from bootstrap.types import App
from config.environment import EnvironmentConfigLoader
from config.types import EnvironmentConfig
from database import RedisRepository, IKeyValueRepository


class Bootstrap:

    @staticmethod
    def _load_env_config() -> EnvironmentConfig:
        loader = EnvironmentConfigLoader()
        config = loader.load()
        return config

    @staticmethod
    def initialize_storage(host: str, port: int) -> IKeyValueRepository:
        return RedisRepository(host=host, port=port, db=0)

    def initialize_app(self) -> App:
        config = self._load_env_config()
        storage = self.initialize_storage(
            host=config.redis.host,
            port=config.redis.port,
        )
        return App(
            config=config,
            storage=storage,
        )

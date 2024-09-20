from bootstrap.types import App
from config.environment import EnvironmentConfigLoader
from config.types import EnvironmentConfig


class Bootstrap:

    @staticmethod
    def load_env_config() -> EnvironmentConfig:
        loader = EnvironmentConfigLoader()
        config = loader.load()
        return config

    def initialize_app(self) -> App:
        config = self.load_env_config()
        return App(
            config=config,
        )
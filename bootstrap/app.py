import logging
import sys
from pathlib import Path

from bootstrap.types import App, LoggerGroup
from bot.loader import BotLoader
from bot.types import Bot
from config import ConfigLoader
from config.environment import EnvironmentConfigLoader
from config.settings import SettingsLoader
from config.types import Config
from database import IKeyValueRepository
from database.redis import RedisRepository
from services.auth.token_managers import TokenManager, ITokenManager


class Bootstrap:
    LOGS_BASE_DIR = Path("./logs/")

    @staticmethod
    def _init_config() -> Config:
        loader = ConfigLoader(
            env_loader=EnvironmentConfigLoader(),
            settings_loader=SettingsLoader(),
        )
        return loader.load()

    @staticmethod
    def _init_storage(config: Config) -> IKeyValueRepository:
        storage = RedisRepository(
            host=config.env.redis.host, port=config.env.redis.port, db=0
        )
        return storage

    @staticmethod
    def _init_token_manager(storage: IKeyValueRepository) -> ITokenManager:
        token_storage = TokenManager(storage)
        return token_storage

    @staticmethod
    def _init_bot(config: Config, logger_group: LoggerGroup) -> Bot:
        bot_loader = BotLoader(config=config, logger_group=logger_group)
        return bot_loader.load()

    @staticmethod
    def _configure_logging() -> None:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    @classmethod
    def __init_logger(cls, path: str, config: Config) -> logging.Logger:
        path_parts = path.split("/")
        logger_name = (path_parts[-1]).split(".")[0]

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler(cls.LOGS_BASE_DIR / path, mode="a")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(config.settings.logging.format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _init_logger_group(self, config: Config) -> LoggerGroup:
        general = self.__init_logger("general.log", config)
        return LoggerGroup(
            general=general,
        )

    def initialize_app(self) -> App:
        config = self._init_config()
        storage = self._init_storage(config)
        token_manager = self._init_token_manager(storage)
        logger_group = self._init_logger_group(config)
        bot = self._init_bot(config, logger_group)

        self._configure_logging()

        return App(
            config=config,
            storage=storage,
            token_manager=token_manager,
            bot=bot,
            logger_group=logger_group,
        )

import logging
import sys
from pathlib import Path

from src.bootstrap.types import App, LoggerGroup
from src.bot.loader import BotLoader
from src.bot.types import Bot
from src.config import ConfigLoader
from src.config.environment import EnvironmentConfigLoader
from src.config.settings import SettingsLoader
from src.config.types import Config
from src.database import IKeyValueRepository
from src.database.redis import RedisRepository
from src.services.business.token_manager import TokenManager, ITokenManager


class Bootstrap:
    LOGS_BASE_DIR = Path("./logs/")

    @staticmethod
    async def _init_config() -> Config:
        loader = ConfigLoader(
            env_loader=EnvironmentConfigLoader(),
            settings_loader=SettingsLoader(),
        )
        return loader.load()

    @staticmethod
    async def _init_storage(config: Config) -> IKeyValueRepository:
        storage = RedisRepository(
            host=config.env.redis.host, port=config.env.redis.port, db=0
        )
        return storage

    @staticmethod
    async def _init_token_manager(storage: IKeyValueRepository) -> ITokenManager:
        return TokenManager(storage)

    @staticmethod
    async def _init_bot(
        config: Config,
        logger_group: LoggerGroup,
    ) -> Bot:
        bot_loader = BotLoader(
            config=config,
            logger_group=logger_group,
        )
        return await bot_loader.load()


    @staticmethod
    async def _configure_logging() -> None:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    @classmethod
    async def __init_logger(cls, path: str, config: Config) -> logging.Logger:
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

    async def _init_logger_group(self, config: Config) -> LoggerGroup:
        general = await self.__init_logger("general.log", config)
        return LoggerGroup(
            general=general,
        )

    async def initialize_app(self) -> App:
        config = await self._init_config()
        storage = await self._init_storage(config)
        logger_group = await self._init_logger_group(config)
        token_manager = await self._init_token_manager(storage)
        bot = await self._init_bot(config, logger_group)

        await self._configure_logging()

        return App(
            config=config,
            storage=storage,
            logger_group=logger_group,
            bot=bot,
        )

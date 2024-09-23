import logging
import sys
from pathlib import Path

from aiogram.utils.i18n import I18n

from src.bootstrap.types import App, LoggerGroup, Services
from src.bot.loader import BotLoader
from src.bot.types import Bot
from src.config import ConfigLoader
from src.config.environment import EnvironmentConfigLoader
from src.config.settings import SettingsLoader
from src.config.types import Config
from src.database import IKeyValueRepository
from src.database.redis import RedisRepository
from src.services.api.auth import AuthAPIClient
from src.services.business.auth import AuthService
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
        services: Services,
        i18n: I18n,
    ) -> Bot:
        bot_loader = BotLoader(
            config=config,
            logger_group=logger_group,
            services=services,
            i18n=i18n,
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

    @staticmethod
    async def _init_services(config: Config, token_manager: ITokenManager) -> Services:
        auth_api_client = AuthAPIClient(base_url=config.env.api.base_url)
        auth_service = AuthService(auth_api_client, token_manager)

        return Services(
            auth=auth_service,
        )

    @staticmethod
    async def _init_i18n(config: Config) -> I18n:
        return I18n(
            path=config.settings.localization.locales_path,
            default_locale=config.settings.localization.default_locale,
            domain=config.settings.localization.domain,
        )

    async def initialize_app(self) -> App:
        config = await self._init_config()
        storage = await self._init_storage(config)
        logger_group = await self._init_logger_group(config)
        i18n = await self._init_i18n(config)
        token_manager = await self._init_token_manager(storage)
        services = await self._init_services(config, token_manager)
        bot = await self._init_bot(config, logger_group, services, i18n)

        await self._configure_logging()

        return App(
            config=config,
            storage=storage,
            logger_group=logger_group,
            services=services,
            bot=bot,
        )

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
from src.database import KeyValueRepositoryProto
from src.database.redis import RedisRepository
from src.services.api.auth import DefaultAuthAPIClient
from src.services.api.exercises import DefaultExerciseAPIClient
from src.services.api.users import DefaultUserAPIClient
from src.services.api.workouts import DefaultWorkoutAPIClient
from src.services.business.auth import DefaultAuthService
from src.services.business.exercises import DefaultExerciseService
from src.services.business.token_manager import TokenManager, TokenManagerProto
from src.services.business.users import DefaultUserService
from src.services.business.workouts import DefaultWorkoutService


class Bootstrap:
    LOGS_BASE_DIR = Path("./logs/")

    @staticmethod
    async def _init_config() -> Config:
        loader = ConfigLoader(
            env_loader=EnvironmentConfigLoader(),
            settings_loader=SettingsLoader(),
        )
        return await loader.load()

    @staticmethod
    async def _init_storage(config: Config) -> KeyValueRepositoryProto:
        storage = RedisRepository(
            host=config.env.redis.host, port=config.env.redis.port, db=0
        )
        return storage

    @staticmethod
    async def _init_token_manager(
        storage: KeyValueRepositoryProto,
    ) -> TokenManagerProto:
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
    async def _init_services(
        config: Config,
        token_manager: TokenManagerProto,
        storage: KeyValueRepositoryProto,
    ) -> Services:
        auth_api_client = DefaultAuthAPIClient(base_url=config.env.api.base_url)
        user_api_client = DefaultUserAPIClient(base_url=config.env.api.base_url)
        workout_api_client = DefaultWorkoutAPIClient(base_url=config.env.api.base_url)
        exercise_api_client = DefaultExerciseAPIClient(base_url=config.env.api.base_url)

        auth_service = DefaultAuthService(
            auth_api_client, user_api_client, token_manager, storage
        )
        user_service = DefaultUserService(auth_service, user_api_client, token_manager)
        workout_service = DefaultWorkoutService(
            auth_service,
            workout_api_client,
            exercise_api_client,
            token_manager,
            config.settings.validation.exercise,
        )
        exercise_service = DefaultExerciseService(
            auth_service,
            exercise_api_client,
            token_manager,
        )

        return Services(
            auth=auth_service,
            user=user_service,
            workout=workout_service,
            exercise=exercise_service,
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
        services = await self._init_services(config, token_manager, storage)
        bot = await self._init_bot(config, logger_group, services, i18n)

        await self._configure_logging()

        return App(
            config=config,
            storage=storage,
            logger_group=logger_group,
            services=services,
            bot=bot,
        )

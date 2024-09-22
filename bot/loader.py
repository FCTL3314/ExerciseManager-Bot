from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bootstrap.types import LoggerGroup
from bot.handlers import router as base_router
from bot.middlewares import APIClientMiddleware, LoggingMiddleware, ConfigMiddleware
from bot.types import Bot
from config import Config
from services.api.client import IExerciseManagerAPIClient


class IBotLoader(ABC):
    @abstractmethod
    def load(self) -> Bot: ...


class BotLoader(IBotLoader):
    def __init__(
        self,
        config: Config,
        api_client: IExerciseManagerAPIClient,
        logger_group: LoggerGroup,
    ) -> None:
        self._config = config
        self._api_client = api_client
        self._logger_group = logger_group

    def _create_bot(self) -> ABot:
        return ABot(
            token=self._config.env.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    def _create_storage(self) -> RedisStorage:
        return RedisStorage.from_url(self._config.env.redis.uri)

    @staticmethod
    def _create_dispatcher(storage: RedisStorage) -> Dispatcher:
        dp = Dispatcher(storage=storage)
        dp.include_router(base_router)
        return dp

    def _init_middlewares(self, dp: Dispatcher) -> None:
        dp.message.middleware(ConfigMiddleware(self._config))
        # NOTE: Split into different loggers for each miniapp router in the future.
        dp.message.middleware(LoggingMiddleware(self._logger_group.general))
        dp.message.middleware(APIClientMiddleware(self._api_client))

    def load(self) -> Bot:
        bot = self._create_bot()
        storage = self._create_storage()
        dp = self._create_dispatcher(storage)

        self._init_middlewares(dp)

        return Bot(
            client=bot,
            dp=dp,
        )

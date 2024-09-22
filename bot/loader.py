from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bootstrap.types import LoggerGroup
from bot.handlers import router as base_router, unauthorized_callback
from bot.middlewares import APIClientMiddleware, LoggingMiddleware, ConfigMiddleware
from bot.types import Bot
from config import Config
from services.api.client import IExerciseManagerAPIClient


class IBotLoader(ABC):
    @abstractmethod
    async def load(self) -> Bot: ...


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

    async def _create_bot(self) -> ABot:
        return ABot(
            token=self._config.env.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    async def _create_storage(self) -> RedisStorage:
        return RedisStorage.from_url(self._config.env.redis.uri)

    @staticmethod
    async def _create_dispatcher(storage: RedisStorage) -> Dispatcher:
        dp = Dispatcher(storage=storage)
        dp.include_router(base_router)
        return dp

    async def _init_middlewares(self, bot: Bot, dp: Dispatcher) -> None:
        dp.message.middleware(ConfigMiddleware(self._config))
        dp.message.middleware(LoggingMiddleware(self._logger_group.general))
        await self._api_client.set_callback_on_unauthorized(
            lambda user_id: unauthorized_callback(user_id, bot)
        )
        dp.message.middleware(APIClientMiddleware(self._api_client))

    async def load(self) -> Bot:
        bot = await self._create_bot()
        storage = await self._create_storage()
        dp = await self._create_dispatcher(storage)

        await self._init_middlewares(bot, dp)

        return Bot(
            client=bot,
            dp=dp,
        )

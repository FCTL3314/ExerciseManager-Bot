from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.bootstrap.types import LoggerGroup
from src.bot.handlers import router as base_router
from src.bot.middlewares import LoggingMiddleware, ConfigMiddleware
from src.bot.types import Bot
from src.config import Config


class IBotLoader(ABC):
    @abstractmethod
    async def load(self) -> Bot: ...


class BotLoader(IBotLoader):
    def __init__(
        self,
        config: Config,
        logger_group: LoggerGroup,
    ) -> None:
        self._config = config
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

    async def _init_middlewares(self, dp: Dispatcher) -> None:
        dp.message.middleware(ConfigMiddleware(self._config))
        dp.update.outer_middleware(LoggingMiddleware(self._logger_group.general))

    async def load(self) -> Bot:
        bot = await self._create_bot()
        storage = await self._create_storage()
        dp = await self._create_dispatcher(storage)

        await self._init_middlewares(dp)

        return Bot(
            client=bot,
            dp=dp,
        )

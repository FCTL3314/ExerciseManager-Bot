from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import SimpleI18nMiddleware, I18n

from src.bootstrap.types import LoggerGroup, Services
from src.bot.handlers import router as base_router
from src.bot.middlewares import LoggingMiddleware, ConfigMiddleware, ServicesMiddleware
from src.bot.services.lifecycle import on_startup, on_shutdown
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
        services: Services,
        i18n: I18n,
    ) -> None:
        self._config = config
        self._logger_group = logger_group
        self._services = services
        self._i18n = i18n

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
        dp.update.outer_middleware(SimpleI18nMiddleware(self._i18n))
        dp.message.middleware(ServicesMiddleware(self._services))

    @staticmethod
    async def _register_lifecycle(dp: Dispatcher) -> None:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

    async def load(self) -> Bot:
        bot = await self._create_bot()
        storage = await self._create_storage()
        dp = await self._create_dispatcher(storage)

        await self._register_lifecycle(dp)
        await self._init_middlewares(dp)

        return Bot(
            client=bot,
            dp=dp,
        )

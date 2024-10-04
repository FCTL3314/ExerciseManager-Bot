from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import SimpleI18nMiddleware, I18n

from src.bootstrap.types import LoggerGroup, Services
from src.bot.handlers import router as base_router
from src.bot.middlewares import (
    LoggingMiddleware,
    ConfigMiddleware,
    ServicesMiddleware,
    ClearStateOnErrorMiddleware,
    AuthCheckMiddleware,
    RetryOnRateLimitsMiddleware,
)
from src.bot.services.shortcuts.commands import CommandsGroup
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
        commands_group: CommandsGroup,
    ) -> None:
        self._config = config
        self._logger_group = logger_group
        self._services = services
        self._i18n = i18n
        self._commands_group = commands_group

    async def _create_bot(self) -> ABot:
        return ABot(
            token=self._config.env.bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                disable_notification=True,
            ),
        )

    async def _create_storage(self) -> RedisStorage:
        return RedisStorage.from_url(self._config.env.redis.uri)

    @staticmethod
    async def _create_dispatcher(storage: RedisStorage) -> Dispatcher:
        dp = Dispatcher(storage=storage)
        dp.include_router(base_router)
        return dp

    async def load(self) -> Bot:
        bot = await self._create_bot()
        storage = await self._create_storage()
        dp = await self._create_dispatcher(storage)

        return Bot(
            client=bot,
            dp=dp,
            commands_group=self._commands_group,
        )

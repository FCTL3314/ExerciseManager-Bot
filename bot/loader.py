import logging
import sys
from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.handlers import router
from bot.types import Bot
from config import Config


class IBotLoader(ABC):
    @abstractmethod
    def load(self) -> Bot: ...


class BotLoader(IBotLoader):
    def __init__(self, config: Config) -> None:
        self._config = config

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
        dp.include_router(router)
        return dp

    def load(self) -> Bot:
        bot = self._create_bot()
        storage = self._create_storage()
        dp = self._create_dispatcher(storage)

        return Bot(
            client=bot,
            dp=dp,
        )

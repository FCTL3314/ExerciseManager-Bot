from abc import ABC, abstractmethod

from aiogram import Bot as ABot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.types import Bot
from config import Config


class IBotLoader(ABC):

    @abstractmethod
    def load(self) -> Bot: ...


class BotLoader(IBotLoader):
    def __init__(self, config: Config) -> None:
        self._config = config

    def load(self) -> Bot:
        bot = ABot(
            token=self._config.env.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        storage = RedisStorage.from_url(self._config.env.redis.uri)
        dp = Dispatcher(storage=storage)
        return Bot(
            client=bot,
            dp=dp,
        )

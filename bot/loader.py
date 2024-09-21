from aiogram import Bot as ABot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from bot.types import Bot
from config import Config


def initialize_bot(config: Config) -> Bot:
    bot = ABot(token=config.env.bot.token)
    storage = RedisStorage.from_url(config.env.redis.uri)
    dp = Dispatcher(storage=storage)
    return Bot(
        client=bot,
        dp=dp,
    )

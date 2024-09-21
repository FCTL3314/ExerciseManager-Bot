from bot.types import Bot
from config.types import Config

from aiogram import Bot as ABot


def load(config: Config) -> Bot:
    bot = ABot(token=config.env.bot.token)
    return Bot(
        client=bot,
        dp=...,
    )

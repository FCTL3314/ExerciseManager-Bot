from dataclasses import dataclass

from bot.types import Bot
from config.types import Config
from database import IKeyValueRepository


@dataclass
class App:
    config: Config
    storage: IKeyValueRepository
    bot: Bot

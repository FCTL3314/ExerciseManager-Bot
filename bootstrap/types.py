from dataclasses import dataclass
from logging import Logger

from bot.types import Bot
from config.types import Config
from database import IKeyValueRepository


@dataclass
class LoggerGroup:
    general: Logger


@dataclass
class App:
    config: Config
    storage: IKeyValueRepository
    logger_group: LoggerGroup
    bot: Bot

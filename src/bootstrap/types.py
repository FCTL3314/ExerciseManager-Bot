from dataclasses import dataclass
from logging import Logger

from src.bot.types import Bot
from src.config.types import Config
from src.database import IKeyValueRepository


@dataclass
class LoggerGroup:
    general: Logger


@dataclass
class App:
    config: Config
    storage: IKeyValueRepository
    logger_group: LoggerGroup
    bot: Bot

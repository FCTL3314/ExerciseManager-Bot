from dataclasses import dataclass
from logging import Logger

from bot.types import Bot
from config.types import Config
from database import IKeyValueRepository
from services.auth.token_managers import ITokenManager


@dataclass
class LoggerGroup:
    general: Logger


@dataclass
class App:
    config: Config
    storage: IKeyValueRepository
    token_manager: ITokenManager
    bot: Bot
    logger_group: LoggerGroup

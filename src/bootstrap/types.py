from dataclasses import dataclass
from logging import Logger

from src.bot.types import Bot
from src.config.types import Config
from src.database import IKeyValueRepository
from src.services.business.auth import IAuthService


@dataclass(frozen=True)
class LoggerGroup:
    general: Logger


@dataclass(frozen=True)
class Services:
    auth: IAuthService


@dataclass(frozen=True)
class App:
    config: Config
    storage: IKeyValueRepository
    logger_group: LoggerGroup
    services: Services
    bot: Bot

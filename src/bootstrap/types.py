from dataclasses import dataclass
from logging import Logger

from src.bot.types import Bot
from src.config.types import Config
from src.database import IKeyValueRepository
from src.services.business.auth import IAuthService
from src.services.business.users import IUserService
from src.services.business.workouts import IWorkoutService


@dataclass(frozen=True)
class LoggerGroup:
    general: Logger


@dataclass(frozen=True)
class Services:
    auth: IAuthService
    user: IUserService
    workout: IWorkoutService


@dataclass(frozen=True)
class App:
    config: Config
    storage: IKeyValueRepository
    logger_group: LoggerGroup
    services: Services
    bot: Bot

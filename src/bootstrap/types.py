from dataclasses import dataclass
from logging import Logger

from aiogram.utils.i18n import I18n

from src.bootstrap.lifecycle import on_startup, on_shutdown
from src.bot.types import Bot
from src.config.types import Config
from src.database import KeyValueRepositoryProto
from src.services.business.auth import AuthServiceProto
from src.services.business.exercises import ExerciseServiceProto
from src.services.business.users import UserServiceProto
from src.services.business.workouts import WorkoutServiceProto


@dataclass(frozen=True)
class LoggerGroup:
    general: Logger


@dataclass(frozen=True)
class Services:
    auth: AuthServiceProto
    user: UserServiceProto
    workout: WorkoutServiceProto
    exercise: ExerciseServiceProto


@dataclass(frozen=True)
class App:
    config: Config
    storage: KeyValueRepositoryProto
    i18n: I18n
    logger_group: LoggerGroup
    services: Services
    bot: Bot

    async def on_startup(self) -> None:
        await on_startup(
            self.bot,
            self.services,
            self.i18n,
            self.logger_group,
            self.config,
        )

    async def on_shutdown(self) -> None:
        await on_shutdown(self.bot)

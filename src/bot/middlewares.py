from logging import Logger
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from src.bootstrap.types import Services
from src.config import Config


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        data["config"] = self.config
        data["env"] = self.config.env
        data["settings"] = self.config.settings
        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        data["logger"] = self.logger
        return await handler(event, data)


class ServicesMiddleware(BaseMiddleware):
    def __init__(self, services: Services) -> None:
        super().__init__()
        self.services = services

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        data["services"] = self.services
        data["auth_service"] = self.services.auth
        data["user_service"] = self.services.user
        data["workout_service"] = self.services.workout
        data["exercise_service"] = self.services.exercise
        return await handler(event, data)


class ClearStateOnErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            state: FSMContext = data.get("state")
            if state is not None:
                await state.clear()
            raise e

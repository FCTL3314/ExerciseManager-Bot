from logging import Logger
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from bot.exceptions import UserIdRequiredError
from config import Config
from services.api.client import IExerciseManagerAPIClient


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


class APIClientMiddleware(BaseMiddleware):
    def __init__(self, api_client: IExerciseManagerAPIClient) -> None:
        super().__init__()
        self.api_client = api_client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        if (user_id := event.from_user.id) is None:
            raise UserIdRequiredError
        await self.api_client.set_current_tg_user_id(user_id)
        data["api_client"] = self.api_client
        return await handler(event, data)

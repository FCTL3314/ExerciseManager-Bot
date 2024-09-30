from logging import Logger
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message

from src.bootstrap.types import Services
from src.bot.services.shortcuts.commands import CommandsGroup
from src.config import Config
from src.services.business import AuthServiceProto
from src.services.business.exceptions import UnauthorizedError


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


class AuthCheckMiddleware(BaseMiddleware):
    def __init__(
        self,
        commands_group: CommandsGroup,
        auth_service: AuthServiceProto,
    ) -> None:
        self._auth_service = auth_service
        self._commands_group = commands_group

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        message_text = event.message.text
        tg_user_id = event.message.from_user.id

        for command in self._commands_group.commands:

            if not command.is_match(message_text):
                continue

            if not command.require_auth:
                continue

            user_id = await self._auth_service.get_user_id_by_tg_user_id(
                tg_user_id=tg_user_id
            )
            if user_id is None:
                raise UnauthorizedError

        return await handler(event, data)

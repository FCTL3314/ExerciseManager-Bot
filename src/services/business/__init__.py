from abc import ABC
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, Awaitable

from aiohttp import ClientResponseError

from src.services.business.auth import IAuthService
from src.services.business.exceptions import (
    InheritanceRequiredForDecoratorError,
)
from src.services.business.token_manager import ITokenManager


class BaseService(ABC):
    def __init__(self, auth_service: IAuthService) -> None:
        self._auth_service = auth_service

    @staticmethod
    def refresh_tokens_on_unauthorized(method: Callable[..., Awaitable[Any]]):
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            if not isinstance(self, BaseService):
                raise InheritanceRequiredForDecoratorError(
                    f"This decorator should only be used on methods "
                    f"of classes inheriting from {BaseService.__name__}."
                )

            if not (user_id := kwargs.get("user_id")):
                raise TypeError("Missing required 'user_id' argument.")

            try:
                return await method(self, *args, **kwargs)
            except ClientResponseError as e:
                if e.status != HTTPStatus.UNAUTHORIZED:
                    raise e

                is_tokens_refreshed = await self._auth_service.refresh_tokens(
                    user_id=user_id
                )

                if not is_tokens_refreshed:
                    raise e

                return await method(self, *args, **kwargs)

        return wrapper

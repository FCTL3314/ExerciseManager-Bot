from logging import Logger
from typing import Callable, Coroutine

from starlette.requests import Request

from src.bot.types import Bot
from src.config import Config


async def get_enrich_state_middleware(
    config: Config,
    bot: Bot,
    logger: Logger,
) -> Callable:
    async def enrich_state_middleware(request: Request, call_next) -> Coroutine:
        request.state.config = config
        request.state.dp = bot.dp
        request.state.bot = bot.client
        request.state.logger = logger
        return await call_next(request)

    return enrich_state_middleware

from asyncio import AbstractEventLoop
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from fastapi import FastAPI
from uvicorn import Server, Config as UvicornConfig

from src.bootstrap.types import LoggerGroup, Services
from src.bot.services.lifecycle import (
    on_startup as on_bot_startup,
    on_shutdown as on_bot_shutdown,
)
from src.bot.types import Bot
from src.config import Config
from src.server.controllers import router
from src.server.middlewares import get_enrich_state_middleware


class ServerRunner:

    def __init__(
        self,
        bot: Bot,
        services: Services,
        logger_group: LoggerGroup,
        config: Config,
    ) -> None:
        self._app = FastAPI(lifespan=self._lifespan)
        self._bot = bot
        self._services = services
        self._logger_group = logger_group
        self._config = config

    async def _register_middlewares(self) -> None:
        enrich_state_middleware = await get_enrich_state_middleware(
            self._config,
            self._bot,
            self._logger_group.general,
        )

        self._app.middleware("http")(enrich_state_middleware)

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncContextManager[None]:
        await on_bot_startup(self._bot.client, self._bot.commands_group)
        yield
        await on_bot_shutdown(self._bot.client)

    async def _before_start(self) -> None:
        self._app.include_router(router)
        await self._register_middlewares()

    async def run_server(self, loop: AbstractEventLoop) -> None:
        await self._before_start()
        config = UvicornConfig(
            app=self._app,
            host="127.0.0.1",
            port=8000,
            loop=loop,  # noqa
        )
        server = Server(config)
        await server.serve()

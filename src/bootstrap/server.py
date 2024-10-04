from asyncio import AbstractEventLoop
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from fastapi import FastAPI
from uvicorn import Server, Config as UvicornConfig

from src.bootstrap.types import App
from src.server.controllers import router
from src.server.middlewares import get_enrich_state_middleware


class ServerRunner:

    def __init__(self, app: App) -> None:
        self.app = app
        self.api = FastAPI(lifespan=self._lifespan)

    async def _register_middlewares(self) -> None:
        enrich_state_middleware = await get_enrich_state_middleware(
            self.app.config,
            self.app.bot,
            self.app.logger_group.general,
        )

        self.api.middleware("http")(enrich_state_middleware)

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncContextManager[None]:
        await self.app.on_startup()
        yield
        await self.app.on_shutdown()

    async def _before_start(self) -> None:
        self.api.include_router(router)
        await self._register_middlewares()

    async def run_server(self, loop: AbstractEventLoop) -> None:
        await self._before_start()
        config = UvicornConfig(
            app=self.api,
            host="127.0.0.1",
            port=8000,
            loop=loop,  # noqa
        )
        server = Server(config)
        await server.serve()

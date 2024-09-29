from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI

from src.bootstrap import AppInitializerProto
from src.server.controllers.webhooks import register_telegram_updates_webhook


class ServerRunner:

    def __init__(self, app_initializer: AppInitializerProto) -> None:
        self.app = FastAPI(lifespan=self.lifespan)
        self.app_initializer = app_initializer

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncContextManager[None]:
        _app = await self.app_initializer.init_app()
        await register_telegram_updates_webhook(
            app, _app.bot.client, _app.bot.dp, _app.config
        )
        yield

    def run_server(self) -> None:
        uvicorn.run(self.app, host="127.0.0.1", port=8000)

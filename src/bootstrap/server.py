from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI

from src.bootstrap import AppInitializerProto
from src.bot.services.lifecycle import (
    on_startup as on_bot_startup,
    on_shutdown as on_bot_shutdown,
)
from src.server.controllers.webhooks import register_telegram_updates_webhook


class ServerRunner:

    def __init__(self, app_initializer: AppInitializerProto) -> None:
        self.app = FastAPI(lifespan=self.lifespan)
        self.app_initializer = app_initializer

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncContextManager[None]:
        _app = await self.app_initializer.init_app()
        await on_bot_startup(_app.bot.client, _app.bot.commands_group)
        await register_telegram_updates_webhook(
            app,
            _app.bot.client,
            _app.bot.dp,
            _app.config,
            _app.logger_group.general,
            ignore_errors=True,
        )
        yield
        await on_bot_shutdown(_app.bot.client)

    def run_server(self) -> None:
        uvicorn.run(self.app, host="127.0.0.1", port=8000)

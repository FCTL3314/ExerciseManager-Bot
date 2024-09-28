from http import HTTPStatus

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.config import Config


async def init_tg_update_webhook(
    app: FastAPI,
    bot: Bot,
    dp: Dispatcher,
    config: Config,
) -> None:
    @app.post(config.env.bot.webhook_path)
    async def webhook(request: Request, token: str) -> None:
        if token != config.env.bot.token:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invalid token",
            )

        header = config.settings.server.telegram_secret_token_header
        if request.headers.get(header) != config.env.bot.webhook_secret:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invalid secret token",
            )

        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)

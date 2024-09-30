from http import HTTPStatus
from logging import Logger

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from src.config import Config


async def register_telegram_updates_webhook(
    app: FastAPI,
    bot: Bot,
    dp: Dispatcher,
    config: Config,
    logger: Logger,
    ignore_errors: bool = False,
) -> None:
    @app.post(config.env.bot.webhook_path)
    async def telegram_updates_webhook(request: Request, token: str) -> None:
        try:
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
        except Exception as e:
            logger.exception(e)
            if not ignore_errors:
                raise e
            Response(status_code=HTTPStatus.OK)

from http import HTTPStatus
from logging import Logger

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from src.bot.types import Bot
from src.config import Config
from src.constants import TELEGRAM_UPDATES_WEBHOOK_PATH
from src.server.controllers.webhooks import router
from src.server.dependencies import (
    config_dependency,
    dispatcher_dependency,
    bot_dependency,
    logger_dependency,
)


@router.post(TELEGRAM_UPDATES_WEBHOOK_PATH)
async def telegram_updates_webhook(
    request: Request,
    token: str,
    config: Config = config_dependency,
    dp: Dispatcher = dispatcher_dependency,
    bot: Bot = bot_dependency,
    logger: Logger = logger_dependency,
) -> None:
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
    Response(status_code=HTTPStatus.OK)

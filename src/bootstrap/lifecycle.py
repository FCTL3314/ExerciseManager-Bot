from typing import TYPE_CHECKING

from aiogram.utils.i18n import I18n

from src.bot.services.lifecycle import (
    on_startup as on_bot_startup,
    on_shutdown as on_bot_shutdown,
)
from src.bot.types import Bot
from src.config import Config


if TYPE_CHECKING:
    from src.bootstrap.types import Services, LoggerGroup


async def on_startup(
    bot: Bot,
    services: "Services",
    i18n: I18n,
    logger_group: "LoggerGroup",
    config: Config,
) -> None:
    await on_bot_startup(
        bot.client,
        bot.dp,
        services,
        i18n,
        logger_group,
        bot.commands_group,
        config,
    )


async def on_shutdown(bot: Bot) -> None:
    await on_bot_shutdown(bot.client)

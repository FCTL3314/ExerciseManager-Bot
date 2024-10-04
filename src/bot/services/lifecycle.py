from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import SimpleI18nMiddleware, I18n

from src.bot.middlewares import (
    ConfigMiddleware,
    ServicesMiddleware,
    RetryOnRateLimitsMiddleware,
    LoggingMiddleware,
    ClearStateOnErrorMiddleware,
    AuthCheckMiddleware,
)
from src.bot.services.shortcuts.commands import (
    CommandsGroup,
)
from src.config import Config


if TYPE_CHECKING:
    from src.bootstrap.types import Services, LoggerGroup


async def _set_bot_commands(bot: Bot, commands_group: CommandsGroup) -> None:
    await bot.set_my_commands(
        commands=[command.as_bot_command() for command in commands_group.commands]
    )


async def _setup_webhook(bot: Bot, config: Config) -> None:
    existed_webhook = await bot.get_webhook_info()
    current_webhook_url = config.env.bot.build_webhook_url_with_token(
        config.env.bot.token
    )

    if existed_webhook.url == current_webhook_url:
        return

    await bot.set_webhook(
        current_webhook_url,
        secret_token=config.env.bot.webhook_secret,
    )


async def _register_middlewares(
    dp: Dispatcher,
    services: "Services",
    i18n: I18n,
    logger_group: "LoggerGroup",
    commands_group: CommandsGroup,
    config: Config,
) -> None:
    dp.update.middleware(ConfigMiddleware(config))
    dp.update.middleware(ServicesMiddleware(services))
    dp.update.middleware(SimpleI18nMiddleware(i18n))
    dp.update.outer_middleware(RetryOnRateLimitsMiddleware())
    dp.update.outer_middleware(LoggingMiddleware(logger_group.general))
    dp.update.outer_middleware(ClearStateOnErrorMiddleware())
    dp.message.outer_middleware(AuthCheckMiddleware(commands_group, services.auth))


async def on_startup(
    bot: Bot,
    dp: Dispatcher,
    services: "Services",
    i18n: I18n,
    logger_group: "LoggerGroup",
    commands_group: CommandsGroup,
    config: Config,
) -> None:
    await _set_bot_commands(bot, commands_group)
    await _setup_webhook(bot, config)
    await _register_middlewares(
        dp, services, i18n, logger_group, commands_group, config
    )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

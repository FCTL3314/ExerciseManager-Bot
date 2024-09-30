from aiogram import Bot

from src.bot.services.shortcuts.commands import (
    CommandsGroup,
)


async def _set_bot_commands(bot: Bot, commands_group: CommandsGroup) -> None:
    await bot.set_my_commands(
        commands=[command.as_bot_command() for command in commands_group.commands]
    )


async def on_startup(bot: Bot, commands_group: CommandsGroup) -> None:
    await _set_bot_commands(bot, commands_group)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

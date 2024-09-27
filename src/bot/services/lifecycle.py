from aiogram import Bot

from src.bot.services.shortcuts.commands import (
    START_COMMAND,
    HELP_COMMAND,
    LOGIN_COMMAND,
    REGISTER_COMMAND,
    ME_COMMAND,
    ADD_WORKOUT_COMMAND,
    ADD_EXERCISE_COMMAND,
    CANCEL_COMMAND,
    WORKOUT_COMMAND,
)


async def _set_bot_commands(bot: Bot) -> None:
    # fmt: off
    await bot.set_my_commands(  # noqa
        commands=[
            START_COMMAND.as_bot_command(),
            HELP_COMMAND.as_bot_command(),
            LOGIN_COMMAND.as_bot_command(),
            REGISTER_COMMAND.as_bot_command(),
            ME_COMMAND.as_bot_command(),
            ADD_WORKOUT_COMMAND.as_bot_command(),
            ADD_EXERCISE_COMMAND.as_bot_command(),
            CANCEL_COMMAND.as_bot_command(),
            WORKOUT_COMMAND.as_bot_command(),
        ]
    )
    # fmt: on


async def on_startup(bot: Bot) -> None:
    await _set_bot_commands(bot)  # noqa


async def on_shutdown(): ...

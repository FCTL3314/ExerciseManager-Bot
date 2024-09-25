from aiogram import Bot
from aiogram.types import BotCommand

from src.bot.services.shortcuts.commands import (
    START_COMMAND,
    HELP_COMMAND,
    LOGIN_COMMAND,
    REGISTER_COMMAND,
    ME_COMMAND,
    ADD_WORKOUT_COMMAND, ADD_EXERCISE_COMMAND,
)


async def _set_bot_commands(bot: Bot) -> None:
    # fmt: off
    await bot.set_my_commands(  # noqa
        commands=[
            BotCommand(command=str(START_COMMAND), description=START_COMMAND.description),
            BotCommand(command=str(HELP_COMMAND), description=HELP_COMMAND.description),
            BotCommand(command=str(LOGIN_COMMAND), description=LOGIN_COMMAND.description),
            BotCommand(command=str(REGISTER_COMMAND), description=REGISTER_COMMAND.description),
            BotCommand(command=str(ME_COMMAND), description=ME_COMMAND.description),
            BotCommand(command=str(ADD_WORKOUT_COMMAND), description=ADD_WORKOUT_COMMAND.description),
            BotCommand(command=str(ADD_EXERCISE_COMMAND), description=ADD_EXERCISE_COMMAND.description),
        ]
    )
    # fmt: on


async def on_startup(bot: Bot) -> None:
    print("Bot is starting up")
    await _set_bot_commands(bot)  # noqa


async def on_shutdown():
    print("Bot is shutting down")

from dataclasses import dataclass

from aiogram import Bot as ABot, Dispatcher

from src.bot.services.shortcuts.commands import CommandsGroup


@dataclass
class Bot:
    client: ABot
    dp: Dispatcher
    commands_group: CommandsGroup

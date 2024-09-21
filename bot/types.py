from dataclasses import dataclass

from aiogram import Bot as ABot, Dispatcher


@dataclass
class Bot:
    client: ABot
    dp: Dispatcher
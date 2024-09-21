from aiogram import Router

router = Router(name=__name__)

from bot.handlers.commands import (
    start,
)

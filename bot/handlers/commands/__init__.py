from aiogram import Router

router = Router(name=__name__)

from bot.handlers.commands.start import *
from bot.handlers.commands.register import *
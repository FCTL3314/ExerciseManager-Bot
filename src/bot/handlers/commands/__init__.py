from aiogram import Router

router = Router(name=__name__)

from src.bot.handlers.commands.start import *
from src.bot.handlers.commands.register import *
from src.bot.handlers.commands.login import *

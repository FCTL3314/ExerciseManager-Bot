from aiogram import Router

router = Router(name=__name__)

from src.bot.handlers.errors.api import *
from src.bot.handlers.errors.common import *

from aiogram import Router

router = Router(name=__name__)

from src.bot.handlers.callback.workout import *
from src.bot.handlers.callback.exercise import *

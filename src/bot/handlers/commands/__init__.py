from aiogram import Router

router = Router(name=__name__)

from src.bot.handlers.commands.common import *
from src.bot.handlers.commands.user import *
from src.bot.handlers.commands.workout import *
from src.bot.handlers.commands.exercise import *

from aiogram import Router

from src.bot.handlers.callback import router as callbacks_router
from src.bot.handlers.commands import router as commands_router
from src.bot.handlers.errors import router as errors_router

router = Router(name=__name__)
router.include_routers(
    commands_router,
    errors_router,
    callbacks_router,
)

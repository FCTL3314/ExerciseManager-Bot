from aiogram import Router

from bot.handlers.commands.start import router as commands_router

router = Router(name=__name__)
router.include_routers(
    commands_router,
)

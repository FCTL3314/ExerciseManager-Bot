import asyncio

from aiogram import Router, Bot, html

from src.bot.handlers.commands.start import router as commands_router

router = Router(name=__name__)
router.include_routers(
    commands_router,
)


async def unauthorized_handler(bot: Bot, user_id: int | str) -> None:
    await bot.send_message(
        user_id,
        f"Вы не авторизованы. Пожалуйста, войдите снова, используя команду {html.bold("/login")}.",
    )


def unauthorized_callback(user_id: int | str, bot: Bot) -> None:
    asyncio.create_task(unauthorized_handler(bot, user_id))

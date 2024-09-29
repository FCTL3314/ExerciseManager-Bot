from logging import Logger

from aiogram import F
from aiogram.types import ErrorEvent, Message

from src.bot.handlers.errors import router


@router.error(F.update.message.as_("message"))
async def common_error_handler(
    event: ErrorEvent, message: Message, logger: Logger
) -> None:
    await message.answer(
        "❗️ Произошла непредвиденная ошибка. Мы уже работаем над её исправлением.\n"
        "Пожалуйста, попробуйте снова позже."
    )
    logger.critical(
        f"Unhandled error caused by {event.exception} in message: {message.text}",
        exc_info=True,
    )

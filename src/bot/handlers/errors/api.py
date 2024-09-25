from http import HTTPStatus
from logging import Logger

from aiogram import html, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
from aiohttp import ClientResponseError

from src.bot.handlers.errors import router


@router.error(ExceptionTypeFilter(ClientResponseError), F.update.message.as_("message"))
async def api_error_handler(event: ErrorEvent, message: Message, logger: Logger):
    status = HTTPStatus(event.exception.status)  # noqa
    match status:
        case HTTPStatus.UNAUTHORIZED:
            await message.answer(
                f"❌ Ваша сессия истекла. Для продолжения работы, пожалуйста, войдите снова, используя команду {html.bold('/login')}."
            )
        case HTTPStatus.FORBIDDEN:
            await message.answer(
                "⛔️ У вас недостаточно прав для выполнения этого действия. Если вы считаете это ошибкой, пожалуйста, свяжитесь с администратором."
            )
        case HTTPStatus.NOT_FOUND:
            await message.answer(
                "🔍 Запрашиваемый ресурс не найден. Пожалуйста, проверьте корректность ввода или попробуйте позже."
            )
        case HTTPStatus.INTERNAL_SERVER_ERROR:
            await message.answer(
                "⚠️ Внутренняя ошибка сервера на стороне внешнего сервиса. Попробуйте повторить запрос позднее."
            )
        case (
            HTTPStatus.BAD_GATEWAY
            | HTTPStatus.SERVICE_UNAVAILABLE
            | HTTPStatus.GATEWAY_TIMEOUT
        ):
            await message.answer(
                "🌐 Внешний сервис временно недоступен. Пожалуйста, повторите попытку позже."
            )
        case _:
            await message.answer(
                f"⚠️ Произошла ошибка при обращении к внешнему ресурсу. Статус: {status}. Попробуйте позже."
            )
            logger.warning(
                f"Unhandled backend request error:",
                exc_info=True,
            )

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.handlers.commands import router


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет 👋, {html.bold(message.from_user.full_name)}!\n\n"
        "Я твой личный фитнес-ассистент 🤸🏻‍♀️️. "
        "Вместе мы создадим эффективные тренировочные программы, добавим упражнения 🏃‍♂️ и будем отслеживать твой прогресс 📊. "
        "Я напомню, когда нужно сделать перерыв 🛌, и подскажу, когда пора продолжать 🏃‍♀️.\n\n"
        f"Готов начать тренировки? 🎯 "
        f"Для этого зарегистрируйся с помощью команды {html.bold("/register")} или войди через {html.bold("/login")}"
    )

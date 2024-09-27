from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.services.shortcuts.commands import CANCEL_COMMAND


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


@router.message(CANCEL_COMMAND.filter())
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🚫 Операция отменена. Если хотите начать заново, введите соответствующую команду."
    )

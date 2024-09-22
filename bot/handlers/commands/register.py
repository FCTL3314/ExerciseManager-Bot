from logging import Logger

from aiogram import html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.commands import router
from bot.states import RegistrationStates


@router.message(Command("register"))
async def command_register_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(RegistrationStates.username)
    await message.answer(
        "Добро пожаловать в процесс регистрации! 📝\n\n"
        "1️⃣ Для начала, пожалуйста, введите ваше имя пользователя:"
    )


@router.message(RegistrationStates.username)
async def process_username(message: Message, state: FSMContext) -> None:
    username = message.text
    await state.update_data(username=username)
    await state.set_state(RegistrationStates.password)
    await message.answer(
        f"Отлично, {html.bold(username)}! ✅\n\n"
        "2️⃣ Теперь введите пароль для завершения регистрации:"
    )


@router.message(RegistrationStates.password)
async def process_password(message: Message, state: FSMContext) -> None:
    password = message.text
    await state.update_data(password=password)
    await state.set_state(RegistrationStates.password_retype)
    await message.answer("3️⃣ Теперь повторите введенный пароль:")


@router.message(RegistrationStates.password_retype)
async def process_password_retype(message: Message, state: FSMContext) -> None:
    retyped_password = message.text
    data = await state.get_data()
    original_password = data.get("password")

    if retyped_password != original_password:
        await message.answer(
            "❌ Пароли не совпадают. Пожалуйста, попробуйте снова.\n\n"
            "Введите пароль еще раз:"
        )
        await state.set_state(RegistrationStates.password)
    else:
        await state.clear()
        await message.answer("Пароль принят! ✅")
        await message.answer(
            "Регистрация успешно завершена! 🎉\n\n"
            "Теперь вы можете использовать свои данные для входа в систему. "
            "Если возникнут вопросы, напишите команду /help."
        )

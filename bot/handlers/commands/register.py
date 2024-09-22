from aiogram import html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.commands import router
from bot.states import RegistrationStates
from config import Settings
from services.validators.user import is_username_valid, is_password_valid


@router.message(Command("register"))
async def command_register_handler(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    await state.set_state(RegistrationStates.username)
    await message.answer(
        "Добро пожаловать в процесс регистрации! 📝\n\n"
        f"1️⃣ Для начала, пожалуйста, введите ваше имя пользователя "
        f"(от {settings.validation.user.username_min_length} до "
        f"{settings.validation.user.username_max_length} символов):"
    )


@router.message(RegistrationStates.username)
async def process_username(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    username = message.text.strip()
    if not is_username_valid(username, settings.validation.user):
        await message.answer(
            f"❌ Имя пользователя должно быть от "
            f"{settings.validation.user.username_min_length} до "
            f"{settings.validation.user.username_max_length} символов. "
            f"Пожалуйста, попробуйте снова:"
        )
        return

    await state.update_data(username=username)
    await state.set_state(RegistrationStates.password)
    await message.answer(
        f"Отлично, {html.bold(username)}! ✅\n\n"
        f"2️⃣ Теперь введите пароль (от {settings.validation.user.password_min_length} "
        f"до {settings.validation.user.password_max_length} символов):"
    )


@router.message(RegistrationStates.password)
async def process_password(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    password = message.text.strip()
    if not is_password_valid(password, settings.validation.user):
        await message.answer(
            f"❌ Пароль должен быть от {settings.validation.user.password_min_length} "
            f"до {settings.validation.user.password_max_length} символов. "
            f"Пожалуйста, попробуйте снова:"
        )
        return

    await state.update_data(password=password)
    await state.set_state(RegistrationStates.password_retype)
    await message.answer("3️⃣ Повторите введенный пароль для подтверждения:")


@router.message(RegistrationStates.password_retype)
async def process_password_retype(message: Message, state: FSMContext) -> None:
    retyped_password = message.text.strip()
    data = await state.get_data()
    original_password = data.get("password")

    if retyped_password != original_password:
        await message.answer(
            "❌ Пароли не совпадают. Пожалуйста, введите пароль снова:"
        )
        await state.set_state(RegistrationStates.password)
    else:
        await state.clear()
        await message.answer("Пароль подтвержден! ✅")
        await message.answer(
            "Регистрация успешно завершена! 🎉\n\n"
            "Теперь вы можете использовать свои данные для входа в систему. "
            f"Если возникнут вопросы, напишите команду {html.bold("/help")}."
        )

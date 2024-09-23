from aiogram import html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.message_templates import (
    INVALID_USERNAME_TEMPLATE,
    INVALID_PASSWORD_TEMPLATE,
)
from src.bot.shurtcuts.commands import (
    REGISTER_COMMAND,
    LOGIN_COMMAND,
    HELP_COMMAND,
)
from src.bot.states import RegistrationStates
from src.config import Settings
from src.services.business.auth import IAuthService
from src.services.business.exceptions import PasswordsDoNotMatchError
from src.services.validators.user import is_username_valid, is_password_valid


@router.message(Command(REGISTER_COMMAND.name))
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
            INVALID_USERNAME_TEMPLATE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            ),
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
            INVALID_PASSWORD_TEMPLATE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            ),
        )
        return

    await state.update_data(password=password)
    await state.set_state(RegistrationStates.password_retype)
    await message.answer("3️⃣ Повторите введенный пароль для подтверждения:")


@router.message(RegistrationStates.password_retype)
async def process_password_retype(
    message: Message, state: FSMContext, auth_service: IAuthService
) -> None:
    data = await state.get_data()

    username = data["username"]
    original_password = data["password"]
    retyped_password = message.text.strip()

    try:
        await auth_service.register(username, original_password, retyped_password)
        await message.answer(
            "Регистрация успешно завершена! 🎉\n\n"
            f"Теперь вы можете использовать свои данные для входа в систему ({html.bold(LOGIN_COMMAND)}. "
            f"Если возникнут вопросы, напишите команду {html.bold(HELP_COMMAND)}."
        )
        await state.clear()
    except PasswordsDoNotMatchError:
        await message.answer(
            "❌ Пароли не совпадают. Пожалуйста, введите пароль снова:"
        )
        await state.set_state(RegistrationStates.password)

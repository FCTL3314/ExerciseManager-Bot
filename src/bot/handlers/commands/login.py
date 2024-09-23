from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router, LOGIN_COMMAND
from src.bot.message_templates import (
    INVALID_USERNAME_TEMPLATE,
    INVALID_PASSWORD_TEMPLATE,
)
from src.bot.states import LoginStates
from src.config import Settings
from src.services.business.auth import IAuthService
from src.services.validators.user import is_username_valid, is_password_valid


@router.message(Command(LOGIN_COMMAND))
async def command_login_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(LoginStates.username)
    await message.answer(
        "🛂 Добро пожаловать в процесс входа в систему!\n\n"
        "1️⃣ Пожалуйста, введите ваше имя пользователя:"
    )


@router.message(LoginStates.username)
async def process_username(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    username = message.text.strip()
    if not is_username_valid(username, settings.validation.user):
        await message.answer(
            INVALID_USERNAME_TEMPLATE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            )
        )
        return

    await state.update_data(username=username)
    await state.set_state(LoginStates.password)
    await message.answer("2️⃣ Пожалуйста, введите ваш пароль:")


@router.message(LoginStates.password)
async def process_password(
    message: Message,
    state: FSMContext,
    auth_service: IAuthService,
    settings: Settings,
) -> None:
    data = await state.get_data()

    username = data["username"]
    password = message.text.strip()

    if not is_password_valid(password, settings.validation.user):
        await message.answer(
            INVALID_PASSWORD_TEMPLATE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            ),
        )
        return

    is_success = await auth_service.login(message.from_user.id, username, password)
    if is_success:
        await message.answer("✅ Вы успешно вошли в систему! 🎉")
        await state.clear()
    else:
        await message.answer(
            "❌ Неправильное имя пользователя или пароль. Пожалуйста, попробуйте снова."
        )
        await state.clear()

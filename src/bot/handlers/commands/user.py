from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.services.shortcuts.message_templates import (
    INVALID_USERNAME_MESSAGE,
    INVALID_PASSWORD_MESSAGE,
)
from src.bot.services.shortcuts.commands import (
    REGISTER_COMMAND,
    LOGIN_COMMAND,
    HELP_COMMAND,
    ME_COMMAND,
    CANCEL_COMMAND,
)
from src.bot.states.user import RegistrationStates, LoginStates
from src.config import Settings
from src.services.business import AuthServiceProto
from src.services.business.exceptions import PasswordsDoNotMatchError
from src.services.business.users import UserServiceProto
from src.services.validators.user import is_username_valid, is_password_valid


@router.message(REGISTER_COMMAND.filter())
async def command_register_handler(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    await state.set_state(RegistrationStates.waiting_for_username_input)
    await message.answer(
        "Добро пожаловать в процесс регистрации! 📝\n\n"
        f"1️⃣ Для начала, пожалуйста, введите ваше имя пользователя "
        f"(от {settings.validation.user.username_min_length} до "
        f"{settings.validation.user.username_max_length} символов):"
    )


@router.message(RegistrationStates.waiting_for_username_input)
async def process_registration_username(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    username = message.text.strip()
    if not await is_username_valid(username, settings.validation.user):
        await message.answer(
            INVALID_USERNAME_MESSAGE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            ),
        )
        return

    await state.update_data(username=username)
    await state.set_state(RegistrationStates.waiting_for_password_input)
    await message.answer(
        f"Отлично, {html.bold(username)}! ✅\n\n"
        f"2️⃣ Теперь введите пароль (от {settings.validation.user.password_min_length} "
        f"до {settings.validation.user.password_max_length} символов):"
    )


@router.message(RegistrationStates.waiting_for_password_input)
async def process_registration_password(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    await message.delete()
    password = message.text.strip()
    if not await is_password_valid(password, settings.validation.user):
        await message.answer(
            INVALID_PASSWORD_MESSAGE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            ),
        )
        return

    await state.update_data(password=password)
    await state.set_state(RegistrationStates.waiting_for_password_retype_input)
    await message.answer("3️⃣ Повторите введенный пароль для подтверждения:")


@router.message(RegistrationStates.waiting_for_password_retype_input)
async def process_registration_password_retype(
    message: Message, state: FSMContext, auth_service: AuthServiceProto
) -> None:
    await message.delete()
    data = await state.get_data()

    username = data["username"]
    original_password = data["password"]
    retyped_password = message.text.strip()

    try:
        await auth_service.register(
            username=username,
            password=original_password,
            retyped_password=retyped_password,
        )
        await message.answer(
            "Регистрация успешно завершена! 🎉\n\n"
            f"Теперь вы можете использовать свои данные для входа в систему {html.bold(LOGIN_COMMAND)}. "
            f"Если возникнут вопросы, напишите команду {html.bold(HELP_COMMAND)}."
        )
        await state.clear()
    except PasswordsDoNotMatchError:
        await message.answer(
            "❌ Пароли не совпадают. Пожалуйста, введите пароль снова:"
        )
        await state.set_state(RegistrationStates.waiting_for_password_input)


@router.message(LOGIN_COMMAND.filter())
async def command_login_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(LoginStates.waiting_for_username_input)
    await message.answer(
        "👤 Добро пожаловать в процесс входа в систему!\n\n"
        "1️⃣ Пожалуйста, введите ваше имя пользователя:"
    )


@router.message(LoginStates.waiting_for_username_input)
async def process_login_username(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    username = message.text.strip()
    if not await is_username_valid(username, settings.validation.user):
        await message.answer(
            INVALID_USERNAME_MESSAGE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            )
        )
        return

    await state.update_data(username=username)
    await state.set_state(LoginStates.waiting_for_password_input)
    await message.answer("2️⃣ Пожалуйста, введите ваш пароль:")


@router.message(LoginStates.waiting_for_password_input)
async def process_login_password(
    message: Message,
    state: FSMContext,
    auth_service: AuthServiceProto,
    settings: Settings,
) -> None:
    await message.delete()
    data = await state.get_data()

    username = data["username"]
    password = message.text.strip()

    if not await is_password_valid(password, settings.validation.user):
        await message.answer(
            INVALID_PASSWORD_MESSAGE.format(
                min_length=settings.validation.user.username_min_length,
                max_length=settings.validation.user.username_max_length,
            ),
        )
        return

    processing_message = await message.answer("⏳ Пароль принят, обработка...")

    is_success = await auth_service.login(
        user_id=message.from_user.id, username=username, password=password
    )
    if is_success:
        await processing_message.edit_text("🎉 Вы успешно вошли в систему!")
        await state.clear()
    else:
        await processing_message.edit_text(
            f"❌ Неправильное имя пользователя или пароль. Пожалуйста, введите пароль снова, или выполните команду ({html.bold(CANCEL_COMMAND)})."
        )
        return


@router.message(ME_COMMAND.filter())
async def command_me_handler(message: Message, user_service: UserServiceProto) -> None:
    me = await user_service.me(user_id=message.from_user.id)

    created_at_formatted = me.created_at.strftime("%d %B %Y")

    await message.answer(
        f"👤 {html.bold("Your Profile")}:\n\n"
        f"🆔 {html.bold("ID")}: {me.id}\n"
        f"👤 {html.bold("Username")}: {me.username}\n"
        f"📅 {html.bold("Registered on")}: {created_at_formatted}"
    )

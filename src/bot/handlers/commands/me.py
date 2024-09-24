from aiogram import html
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.services.shortcuts.commands import ME_COMMAND
from src.services.business.users import IUserService


@router.message(Command(ME_COMMAND.name))
async def command_me_handler(message: Message, user_service: IUserService) -> None:
    me = await user_service.me(message.from_user.id)

    created_at_formatted = me.created_at.strftime("%d %B %Y")

    await message.answer(
        f"👤 {html.bold("Your Profile")}:\n\n"
        f"🆔 {html.bold("ID")}: {me.id}\n"
        f"👤 {html.bold("Username")}: {me.username}\n"
        f"📅 {html.bold("Registered on")}: {created_at_formatted}"
    )

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.handlers.commands import router


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

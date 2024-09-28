from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.services.shortcuts.commands import CANCEL_COMMAND
from src.bot.services.shortcuts.message_templates import START_MESSAGE, CANCELED_MESSAGE


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(START_MESSAGE.format(name=message.from_user.full_name))


@router.message(CANCEL_COMMAND.filter())
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(CANCELED_MESSAGE)

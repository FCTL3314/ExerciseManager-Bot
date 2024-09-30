from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_base_skip_keyboard(
    callback: CallbackData, text: str = "⏭️ Пропустить"
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback.pack(),
                )
            ]
        ],
    )

from aiogram.types import InlineKeyboardMarkup


def combine_keyboards(
    *keyboards: InlineKeyboardMarkup,
    **kwargs,
) -> InlineKeyboardMarkup:
    combined_inline_keyboard = [
        button for keyboard in keyboards for button in keyboard.inline_keyboard
    ]

    return InlineKeyboardMarkup(
        **kwargs,
        inline_keyboard=combined_inline_keyboard,
    )

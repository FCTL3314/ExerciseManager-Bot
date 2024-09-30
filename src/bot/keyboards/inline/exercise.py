from aiogram.types import InlineKeyboardMarkup

from src.bot.callbacks import SkipExerciseDescriptionCallback, SkipExerciseImageCallback
from src.bot.keyboards.inline import create_base_skip_keyboard


async def get_skip_exercise_description_keyboard() -> InlineKeyboardMarkup:
    return await create_base_skip_keyboard(SkipExerciseDescriptionCallback())


async def get_skip_exercise_image_keyboard() -> InlineKeyboardMarkup:
    return await create_base_skip_keyboard(SkipExerciseImageCallback())

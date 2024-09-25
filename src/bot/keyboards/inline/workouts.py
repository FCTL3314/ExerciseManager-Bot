from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks import WorkoutsSelectCallback
from src.models.workout import Workout


async def get_workouts_keyboard(workouts: list[Workout]) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=workout.name,
            callback_data=WorkoutsSelectCallback(workout_id=workout.id).pack(),
        )
        for workout in workouts
    ]
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[buttons])

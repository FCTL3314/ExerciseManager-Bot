from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks import (
    SkipExerciseDescriptionCallback,
    SkipExerciseImageCallback,
    SkipWorkoutExerciseCallback,
)
from src.bot.keyboards.inline import create_base_skip_keyboard
from src.bot.keyboards.inline.workouts import (
    create_pause_workout_keyboard,
    create_resume_workout_keyboard,
)
from src.bot.services.keyboards import combine_keyboards


async def create_skip_exercise_description_keyboard() -> InlineKeyboardMarkup:
    return await create_base_skip_keyboard(SkipExerciseDescriptionCallback())


async def create_skip_exercise_image_keyboard() -> InlineKeyboardMarkup:
    return await create_base_skip_keyboard(SkipExerciseImageCallback())


async def create_skip_workout_exercise_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏭️ Пропустить",
                    callback_data=SkipWorkoutExerciseCallback().pack(),
                )
            ]
        ],
    )


async def create_active_workout_keyboard() -> InlineKeyboardMarkup:
    return combine_keyboards(
        await create_pause_workout_keyboard(),
        await create_skip_workout_exercise_keyboard(),
        row_width=1,
    )


async def create_paused_workout_keyboard() -> InlineKeyboardMarkup:
    return combine_keyboards(
        await create_resume_workout_keyboard(),
        await create_skip_workout_exercise_keyboard(),
        row_width=1,
    )

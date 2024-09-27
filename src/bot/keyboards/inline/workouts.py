from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks import (
    WorkoutsSelectCallback,
    WorkoutsPaginationCallback,
    DisabledCallback,
    StartWorkoutCallback,
)
from src.services.business.workouts import WorkoutServiceProto
from src.services.collections import chunk_list
from src.services.exceptions import NoWorkoutsError


async def get_select_workout_keyboard(
    user_id: int | str,
    workout_service: WorkoutServiceProto,
    buttons_per_row: int,
    limit: int,
    offset: int = 0,
) -> InlineKeyboardMarkup:
    paginated_workouts = await workout_service.list(
        user_id=user_id, limit=limit, offset=offset
    )

    if not paginated_workouts.results:
        raise NoWorkoutsError

    workouts_btns = [
        InlineKeyboardButton(
            text=workout.name,
            callback_data=WorkoutsSelectCallback(workout_id=workout.id).pack(),
        )
        for workout in paginated_workouts.results
    ]

    pagination_btns = [
        InlineKeyboardButton(
            text="⬅️ Назад" if paginated_workouts.has_previous else "🔒 Назад",
            callback_data=(
                WorkoutsPaginationCallback(
                    offset=paginated_workouts.previous_offset,
                ).pack()
                if paginated_workouts.has_previous
                else DisabledCallback().pack()
            ),
        ),
        InlineKeyboardButton(
            text="Вперёд ➡️" if paginated_workouts.has_next else "🔒 Вперёд",
            callback_data=(
                WorkoutsPaginationCallback(
                    offset=paginated_workouts.next_offset,
                ).pack()
                if paginated_workouts.has_next
                else DisabledCallback().pack()
            ),
        ),
    ]

    final_btns = [
        *chunk_list(workouts_btns, buttons_per_row),
        pagination_btns,
    ]

    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=final_btns,
    )


async def get_start_workout_keyboard() -> InlineKeyboardMarkup:
    btns = [
        [
            InlineKeyboardButton(
                text="🚀 Начать тренировку",
                callback_data=StartWorkoutCallback().pack(),
            )
        ]
    ]

    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=btns,
    )

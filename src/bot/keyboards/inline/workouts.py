from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks import WorkoutsSelectCallback, WorkoutsPaginationCallback
from src.services.business.workouts import WorkoutServiceProto
from src.services.collections import chunk_list
from src.services.exceptions import NoWorkoutsError


async def get_workouts_keyboard(
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

    pagination_btns = []

    if paginated_workouts.has_previous:
        pagination_btns.append(
            InlineKeyboardButton(
                text="⬅️ Предыдущая",
                callback_data=WorkoutsPaginationCallback(
                    offset=paginated_workouts.previous_offset,
                ).pack(),
            )
        )

    if paginated_workouts.has_next:
        pagination_btns.append(
            InlineKeyboardButton(
                text="Следующая ➡️",
                callback_data=WorkoutsPaginationCallback(
                    offset=paginated_workouts.next_offset,
                ).pack(),
            )
        )

    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[*chunk_list(workouts_btns, buttons_per_row), pagination_btns],
    )

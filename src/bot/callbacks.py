from aiogram.filters.callback_data import CallbackData


class WorkoutsSelectCallback(CallbackData, prefix="selected_workout"):
    workout_id: int


class WorkoutsPaginationCallback(CallbackData, prefix="workout_pagination"):
    offset: int

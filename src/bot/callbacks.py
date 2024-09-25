from aiogram.filters.callback_data import CallbackData


class SelectedWorkout(CallbackData, prefix="selected_workout"):
    workout_id: int

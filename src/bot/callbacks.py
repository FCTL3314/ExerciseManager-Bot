from aiogram.filters.callback_data import CallbackData


class DisabledCallback(CallbackData, prefix="disabled"): ...


class WorkoutsSelectCallback(CallbackData, prefix="selected_workout"):
    workout_id: int


class WorkoutsPaginationCallback(CallbackData, prefix="workout_pagination"):
    offset: int


class NextExerciseCallback(CallbackData, prefix="next_exercise"): ...

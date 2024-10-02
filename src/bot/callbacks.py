from aiogram.filters.callback_data import CallbackData


class DisabledCallback(CallbackData, prefix="disabled"): ...


class WorkoutsSelectCallback(CallbackData, prefix="selected_workout"):
    workout_id: int


class WorkoutsPaginationCallback(CallbackData, prefix="workout_pagination"):
    offset: int


class StartWorkoutCallback(CallbackData, prefix="start_workout"):
    manual_mode_enabled: bool


class PauseWorkoutCallback(CallbackData, prefix="pause_workout"): ...


class ResumeWorkoutCallback(CallbackData, prefix="resume_workout"): ...


class SkipExerciseDescriptionCallback(
    CallbackData, prefix="skip_exercise_description"
): ...


class SkipExerciseImageCallback(CallbackData, prefix="skip_exercise_image"): ...


class NextExerciseCallback(CallbackData, prefix="next_exercise"): ...

class SkipWorkoutExerciseCallback(CallbackData, prefix="skip_workout_exercise"): ...

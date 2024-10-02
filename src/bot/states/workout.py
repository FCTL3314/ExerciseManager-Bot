from aiogram.fsm.state import StatesGroup, State


class WorkoutAddingStates(StatesGroup):
    waiting_for_name_input = State()
    waiting_for_description_input = State()


class ExerciseAddingStates(StatesGroup):
    waiting_for_workout_selection = State()  # TODO: Rename states
    waiting_for_name_input = State()
    waiting_for_description_input = State()
    waiting_for_image_input = State()
    waiting_for_duration_input = State()
    waiting_for_break_time_input = State()


class StartWorkoutStates(StatesGroup):
    selecting_workout = State()
    workout_in_progress = State()
    paused = State()
    skipping_exercise = State()

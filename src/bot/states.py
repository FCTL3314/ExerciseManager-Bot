from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    waiting_for_username_input = State()
    waiting_for_password_input = State()
    waiting_for_password_retype_input = State()


class LoginStates(StatesGroup):
    waiting_for_username_input = State()
    waiting_for_password_input = State()


class WorkoutAddingStates(StatesGroup):
    waiting_for_name_input = State()
    waiting_for_description_input = State()

class ExerciseAddingStates(StatesGroup):
    waiting_for_workout_selection = State()
    waiting_for_name_input = State()
    waiting_for_description_input = State()
    waiting_for_duration_input = State()
    waiting_for_break_time_input = State()


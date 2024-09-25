from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    username = State()
    password = State()
    password_retype = State()


class LoginStates(StatesGroup):
    username = State()
    password = State()


class WorkoutAddingStates(StatesGroup):
    name = State()
    description = State()

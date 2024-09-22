from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    username = State()
    password = State()
    password_retype = State()

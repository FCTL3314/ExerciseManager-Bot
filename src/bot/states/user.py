from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    waiting_for_username_input = State()
    waiting_for_password_input = State()
    waiting_for_password_retype_input = State()


class LoginStates(StatesGroup):
    waiting_for_username_input = State()
    waiting_for_password_input = State()

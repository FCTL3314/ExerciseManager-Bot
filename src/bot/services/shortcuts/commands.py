from aiogram.filters import Command as ACommand
from aiogram.types import BotCommand


class Command:
    def __init__(self, name: str, description: str) -> None:
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def filter(self) -> ACommand:
        return ACommand(self._name)

    def as_bot_command(self) -> BotCommand:
        return BotCommand(command=str(self), description=self._description)

    def __str__(self) -> str:
        return f"/{self.name}"


START_COMMAND = Command(
    "start",
    "Learn more about what I can do for you.",
)
CANCEL_COMMAND = Command(
    "cancel",
    "Cancel current action.",
)
HELP_COMMAND = Command(
    "help",
    "Need assistance? I'll show you how to use my commands.",
)
LOGIN_COMMAND = Command(
    "login",
    "Log in to access your personal data and features tailored just for you.",
)
REGISTER_COMMAND = Command(
    "register",
    "Create an account to unlock all the features and get started.",
)
ME_COMMAND = Command(
    "me",
    "View your profile information and personalized details.",
)
ADD_WORKOUT_COMMAND = Command(
    "add_workout",
    "Create a new workout plan by adding exercises and setting up your routine.",
)
ADD_EXERCISE_COMMAND = Command(
    "add_exercise",
    "Add exercise for your workout.",
)
WORKOUT_COMMAND = Command(
    "workout",
    "Begin your workout session, perform exercises, and track your fitness progress for optimal results.",
)

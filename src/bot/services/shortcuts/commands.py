from aiogram.filters import Command as ACommand
from aiogram.types import BotCommand


class Command:
    def __init__(self, name: str, description: str, require_auth: bool = False) -> None:
        self._name = name
        self._description = description
        self._require_auth = require_auth

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def require_auth(self) -> bool:
        return self._require_auth

    def is_match(self, text: str) -> bool:
        return text.replace("/", "") == self.name

    def filter(self) -> ACommand:
        return ACommand(self._name)

    def as_bot_command(self) -> BotCommand:
        return BotCommand(command=str(self), description=self._description)

    def __str__(self) -> str:
        return f"/{self.name}"


class CommandsGroup:
    def __init__(self) -> None:
        self._commands: list[Command] = []

    @property
    def commands(self) -> list[Command]:
        return self._commands

    def register_command(self, command: Command) -> None:
        self._commands.append(command)


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
    require_auth=True,
)
ADD_WORKOUT_COMMAND = Command(
    "add_workout",
    "Create a new workout plan by adding exercises and setting up your routine.",
    require_auth=True,
)
ADD_EXERCISE_COMMAND = Command(
    "add_exercise",
    "Add exercise for your workout.",
    require_auth=True,
)
START_WORKOUT_COMMAND = Command(
    "start_workout",
    "Begin your workout session, perform exercises, and track your fitness progress for optimal results.",
    require_auth=True,
)


def build_default_commands_group() -> CommandsGroup:
    commands_group = CommandsGroup()
    commands_group.register_command(START_COMMAND)
    commands_group.register_command(CANCEL_COMMAND)
    commands_group.register_command(HELP_COMMAND)
    commands_group.register_command(LOGIN_COMMAND)
    commands_group.register_command(REGISTER_COMMAND)
    commands_group.register_command(ME_COMMAND)
    commands_group.register_command(ADD_WORKOUT_COMMAND)
    commands_group.register_command(ADD_EXERCISE_COMMAND)
    commands_group.register_command(START_WORKOUT_COMMAND)
    return commands_group

class Command:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"/{self.name}"


LOGIN_COMMAND = Command("login")
REGISTER_COMMAND = Command("register")
HELP_COMMAND = Command("help")

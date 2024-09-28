from mypy.semanal_shared import Protocol

from src.bootstrap.types import App


class AppInitializerProto(Protocol):
    """
    Defines a mechanism for setting up the core structure of the Telegram bot application,
    along with any required dependencies and services. The implementation should return
    a fully configured App instance, ready for use within the application lifecycle.
    """

    async def init_app(self) -> App: ...


class ServerRunnerProto(Protocol):
    """
    Defines a mechanism for starting and running the server responsible for managing the
    Telegram bot's operations. The server expects an initialized app via AppInitializerProto
    and handles incoming requests, ensuring the bot's availability and functionality.
    """

    async def run_server(self, app_initializer: AppInitializerProto) -> None: ...

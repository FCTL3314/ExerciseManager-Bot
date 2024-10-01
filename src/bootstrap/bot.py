from aiogram.utils.i18n import I18n

from src.bootstrap.types import LoggerGroup, Services
from src.bot.loader import BotLoader
from src.bot.services.shortcuts.commands import build_default_commands_group
from src.bot.types import Bot
from src.config.types import Config


class BotInitializer:
    def __init__(
        self,
        config: Config,
        logger_group: LoggerGroup,
        services: Services,
        i18n: I18n,
    ):
        self._config = config
        self._logger_group = logger_group
        self._services = services
        self._i18n = i18n

    async def init_bot(self) -> Bot:
        commands_group = build_default_commands_group()
        bot_loader = BotLoader(
            config=self._config,
            logger_group=self._logger_group,
            services=self._services,
            i18n=self._i18n,
            commands_group=commands_group,
        )
        return await bot_loader.load()

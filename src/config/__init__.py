from abc import ABC, abstractmethod

from src.config.types import Config, EnvironmentConfig, Settings


class IEnvironmentConfigLoader(ABC):

    @abstractmethod
    async def load(self) -> EnvironmentConfig: ...


class ISettingsLoader(ABC):

    @abstractmethod
    async def load(self) -> Settings: ...


class ConfigLoader:

    def __init__(
        self,
        env_loader: IEnvironmentConfigLoader,
        settings_loader: ISettingsLoader,
    ) -> None:
        self._env_loader = env_loader
        self._settings_loader = settings_loader

    async def load(self) -> Config:
        env_config = await self._env_loader.load()
        settings = await self._settings_loader.load()
        return Config(
            env=env_config,
            settings=settings,
        )
